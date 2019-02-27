from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from rest_framework import generics
from .models import Game, StoreUser
from .serializers import GameSerializer
from .forms import SignupForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.validators import URLValidator, DecimalValidator, validate_slug
from django.core.exceptions import ValidationError, MultipleObjectsReturned, ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect

from .models import *
from hashlib import md5
import datetime
import time
import json
import re


def main_page(request):
    now = datetime.datetime.now()
    context = { 'time': now }
    return render(request, "main.html", context)


def developer(request, message=""):

    context = {'message':message}

    return render(request, "developer/developer.html", context)


def convert_to_developer(request):

    context = {}

    if request.GET.get('convert', False):
        try:
            user_obj = StoreUser.objects.get(username=request.user.username)
            user_obj.is_developer = True
            user_obj.save()
            return redirect("/dev/")
        except Exception:
            context['message'] = "Could not find an account matching your session user. Are you logged in?"

    return render(request, "developer/convert_to_developer.html", context)



def my_games(request):

    context = {}
    if (request.user.is_authenticated):
        # scrape all games from the user that is logged in.
        owned_games = Game.objects.filter(submitter=request.user)
        context = { 'games' : owned_games }

    return render(request, "developer/my_games.html", context)

def game_sales(request, game_title):

    context = {}

    try:
        game_object = Game.objects.get(title=game_title)
    except ObjectDoesNotExist:
        return developer(request, message="Cannot find sales for the game specified.")

    sales_list = Transaction.objects.filter(game=game_object, is_complete=True)

    context['sales'] = sales_list
    context['game_title'] = game_object.title

    return render(request, "developer/sales.html", context)

def remove_game(request, game_title):

    try:
        game_object = Game.objects.get(title=game_title)
    except ObjectDoesNotExist:
        return developer(request, message="Game could not be found.")

    if game_object.submitter != request.user:
        return developer(request, message="Oops! Did you try removing a game you don't own?")

    game_object.delete()

    return redirect("/dev/my_games/")


def modify_game(request, game_title):

    # finds the game or returns to developer.html with an error.
    try:
        game_object = Game.objects.filter(submitter=request.user).get(title=game_title)
    except ObjectDoesNotExist:
        return developer(request, message="[Error] Game could not be found from your owned games.")

    # method is POST if user has submitted the form.
    if (request.POST):
        return modify_game_submit(request, game_object)


    # if nothing is POSTed we just load the old game data and display it
    context = {
        'game_title'      : game_object.title,
        'game_price'      : game_object.price,
        'game_url'        : game_object.source,
        'game_categories' : game_object.categories.all(),
        'all_categories'  : Category.objects.all(),
    }

    #print(game_object.categories.all())

    return render(request, "developer/modify_game.html", context)

# at this point we can be sure game_object is infact request.user's game
def modify_game_submit(request, game_object):
    data = request.POST
    new_title      = data.get('game_title', False)
    new_price      = data.get('game_price', False)
    new_categories = data.getlist('game_categories')

    if not (new_title and new_price):
        return developer(request, message="Missing required fields.")

    try:
        #game_object.title = new_title

        # validate title
        title_whitelist = r"^[a-zA-Z0-9äöå .,\-!']+$"
        ascii_title = ascii(new_title)
        if not re.search(title_whitelist, ascii_title):
            raise ValidationError("Title contains characters that aren't allowed.")

        new_price = float(new_price)
        if new_price < 0:
            raise ValidationError("Price cannot be negative")

        game_object.price = new_price
        for category_name in new_categories:
            try:
                if not game_object.categories.get(name=category_name).exists():
                    category_obj = Category.objects.get(name=category_name)
                    game_object.categories.add(category_obj)
            except Exception:
                pass

        game_object.save()
    except ValidationError as e:
        return developer(request, message=("Input validation failed. Reason: %s" % e.message))
    except ValueError as e:
        return developer(request, message="Price was not in a proper currency format.")
    except Exception:
        return developer(request, message="There was an error while modifying the game")

    # return to my_games list after making changes to the games
    return my_games(request)
    #return redirect("/dev/modify_game/%s" % game_object.title)

def add_game(request):

    categories = Category.objects.all()

    context = {'categories' : categories}
    return render(request, "developer/add_game.html", context)


def add_game_submit(request):

    if not request.user.is_authenticated:
        return developer(request, message="Please sign in before adding games.")

    data = request.POST

    game_title      = data.get('game_title', False)
    game_price      = data.get('game_price', False)
    game_source     = data.get('game_source', False)
    game_categories = data.getlist('game_categories')

    if not (game_title and game_price and game_source):
        return developer(request, message="Missing required fields.")

    # if url has no http(s)://, prepend it
    http_pattern = "^http[s]{0,1}:\\/\\/"
    if not re.search(http_pattern, game_source):
        game_source = "http://" + game_source


    if game_categories is not None:
        # find category objects matching game_categories
        category_list = []
        for category_name in game_categories:
            try:
                category_obj = Category.objects.get(name=category_name)
                category_list.append(category_obj)
            except ObjectDoesNotExist:
                # if the category doesn't exist, we just skip it. no biggie.
                # this actually only gets triggered if the user tampers with the on-site data
                pass


    # validate title, source and  price.
    # note: we only check if price can be cast to a float and if its positive
    # the actual Game model makes sure the price is in a correct format (max 2 decimal places)
    try:
        # cast price (str) to float
        game_price = float(game_price)
        if game_price < 0:
            raise ValidationError("Price cannot be negative")

        # validate url
        url_val = URLValidator(schemes=None)
        url_val(game_source)

        # validate title
        title_whitelist = r"^[a-zA-Z0-9äöå .,\-!']+$"
        ascii_title = ascii(game_title)
        if not re.search(title_whitelist, ascii_title):
            raise ValidationError("Title contains characters that aren't allowed.")

    except ValidationError as e:
        return developer(request, message=("Input validation failed. Reason: %s" % e.message))
    except ValueError as e:
        return developer(request, message="Price was not in a proper currency format.")

    # make database record
    try:
        new_game = Game(
            title=game_title,
            price=game_price,
            source=game_source,
            submitter=request.user,
        )
        new_game.save()
        request.user.owned_games.add(new_game)
        for category in category_list:
            new_game.categories.add(category)
    except Exception as e:
        # this is only raised if the user has tampered with the client-side input restrictions.
        err_msg = """[Error] OOPSIE WOOPSIE!!\n
        Uwu thewe waz a fucky wucky!! A wittle fucko boingo!\n
        we culd not insert de new game-o to da database :(!!
        model field validations failed...... COULD NOT ADD GAME TO DB..."""

        return developer(request, message=(err_msg))

    return developer(request, message="Successfully added game!")

def hiscores(request, game_title, message=""):
    how_many_scores_to_display = 5 #can set how many scores to display
    index_for_score = -1
    contains = False
    score_objects = Score.objects.filter(game__title__iexact = game_title).order_by('-score')[:how_many_scores_to_display] #get only 5 top scores.
    user_top_score = Score.objects.filter(submitter__username__iexact = request.user.username).order_by('-score')[:1] #get users top score
    all_score_objects = Score.objects.filter(game__title__iexact = game_title).order_by('-score') #get every score for the game


    if not score_objects: #if there are no scores for this game yet
        message = "There are no high scores for this game yet!"

    else:
        for index, score in enumerate(all_score_objects):  #checking if user has a score for the game at all.
            if (score.submitter.username == request.user.username):
                contains = True  #if has containts true
                index_for_score = index + 1

        if contains: #checking if user score is in the top scores, since user already has a score for the game
            contains = False
            for top_score in score_objects:
                if (top_score.submitter.username == request.user.username):
                    contains = True #score is in the top scores


    context = {'game': game_title, 'scores': score_objects, 'user_score': user_top_score, 'contains': contains, 'index': index_for_score, 'message': message}
    return render(request, "hiscores/hiscores_game.html", context)

def hiscores_choose(request, message=""):
    games = Game.objects.all()
    if not games:
        message = "There are currently no games."

    context = {'games': games, 'message': message}
    return render(request, "hiscores/hiscores_choose.html", context)

#Needs to have games in these categories to work
def game_category(request, category_title):
    category = [] #empty set
    categories = Category.objects.filter(name__iexact = category_title)
    if not categories:
        raise Http404 #if no category with the title exist
    else:
        category = categories.get().game_set.all()

    context = { 'category': category, 'category_title': category_title.title() } #gives category name with first letter capitalized
    return render(request, "game_category.html", context)

def game_search(request):
    # get game title (or empty string if 'gamename' not found)
    query = request.GET.get('game_title', '')

    # query the games with a case insensitive contains -filter
    games = Game.objects.filter(title__icontains=query)

    context = {'games' : games}
    return render(request, "game_search.html", context)

def game_page(request, game_title):

    if not request.user.is_authenticated:
        return redirect("/account/login/")

    try:
        game = Game.objects.get(title=game_title)
    except ObjectDoesNotExist:
        raise Http404('Game not found: {}'.format(game_title))

    context = { 'sourceURL': game.source, 'gameTitle': game.title}

    if game not in request.user.owned_games.all():
        return game_not_owned(request, game)

    return render(request, "game.html", context)


def game_not_owned(request, game_object):

    #game_object = Game.objects.get(title=game)

    # payment id (pid) is calculated using current time and buyer username
    # which are hashed using md5 in format [time:buyer_id]
    current_time = str(int(time.time()))
    buyer_id = request.user.username
    pid_string = (current_time + ":" + buyer_id).encode("ascii")
    pid = md5(pid_string).hexdigest()

    new_transaction = Transaction(
        id=pid,
        date=datetime.datetime.now(),
        price=game_object.price,
        is_complete=False,
        buyer=request.user,
        game=game_object
    )
    new_transaction.save()

    # these are constant and should not be modified
    sid = 'LATELATEGAMES'
    secret_code = 'ebee54dffaa4c9249b34fba22154e567'

    amount = game_object.price

    # checksum is calculated using pid, sid, amount and secret_code
    # checksum is sent to the view which is then sent to the payment service.
    checksum = md5(
                "pid={}&sid={}&amount={}&token={}"
                .format(pid, sid, amount, secret_code)
                .encode("ascii")).hexdigest()

    # context (dictionary) is sent to the model "game_not_owned.html"
    context = {
        'checksum': checksum,
        'pid': pid,
        'sid': sid,
        'amount': amount,
        'title': game_object.title
        }
    return render(request, "game_not_owned.html", context)

# view handler for payment result. The transaction can result in: success, fail, cancel
# this handler redirects the user to the correct view based on the url parameter
# payment_result is a string from the url /payment/<payment_result>/
def payment_handler(request, payment_result):

    pid_get = request.GET.get('pid', False)

    if not pid_get:
        raise Http404("PID missing.")

    try:
        transaction = Transaction.objects.get(id=pid_get)

        if transaction.buyer != request.user:
            raise Exception("User did not match pid")

        if transaction.is_complete:
            raise Exception("This transaction has already been processed.")

    except ObjectDoesNotExist:
        raise Http404("Could not find transaction which matches this pid.")
    except Exception as e:
        raise Http404(str(e))



    if (payment_result == "success"):
        return payment_success(request, transaction=transaction)
    elif (payment_result == "error"):
        return payment_error(request, transaction=transaction)
    elif (payment_result == "cancel"):
        return payment_cancel(request, transaction=transaction)
    else:
        raise Http404("Invalid payment result URL.")

def payment_success(request, transaction):
    context = { 'game': transaction.game }

    request.user.owned_games.add(transaction.game)
    transaction.is_complete = True
    transaction.save()

    context = {
        'title': "Success",
        'body' : "You have successfully bought %s" % transaction.game.title
    }

    return render(request, 'payment_response.html', context)

def payment_error(request, transaction):
    context = {
        'title': "Error",
        'body' : """There has been an error with the payment. Please try again.
        If the error persists, please lie down and let out a couple of tears. It may or may not help."""
    }
    return render(request, 'payment_response.html', context)

def payment_cancel(request, transaction):
    context = {
        'title': "Cancelled",
        'body' : "You have cancelled the payment."
        }
    return render(request, 'payment_response.html', context)

class api_games(generics.ListAPIView):
    serializer_class = GameSerializer

    def get_queryset(self):
        queryset = Game.objects.all()
        giventitle = self.request.query_params.get('title', None)
        givenprice = self.request.query_params.get('price', None)
        givensubmitter = self.request.query_params.get('submitter', None)
        if giventitle is not None: queryset =  queryset.filter(title=giventitle)
        if givenprice is not None: queryset =  queryset.filter(price=givenprice)
        if givensubmitter is not None: queryset =  queryset.filter(submitter=givensubmitter)
        return queryset

def save_game_score(request, version):
    if request.method == 'POST':
        try:
            new_score = request.POST.get('score')
            game_title = request.POST.get('title')
            if request.user.is_authenticated:
                new_score = Score(
                    score = new_score,
                    time = datetime.datetime.now(),
                    submitter = request.user,
                    game = Game.objects.get(title=game_title)
                )
                new_score.save()
            return HttpResponse('Ok')
        except:
            console.log('Game score save error.')
            return HttpResponse('Ok')

def get_savedata(user, gameTitle):
    if user.is_authenticated:
        current_game = Game.objects.get(title=gameTitle)
        save = Save.objects.filter(user = user).get(game = current_game)
        return save

def save_game_state(request, version):
    if request.method == 'POST':
        try:
            new_save = request.POST.get('data')
            game_title = request.POST.get('title')
            save = get_savedata(request.user, game_title)
            save.data = new_save
            save.save()
            return HttpResponse('Ok')
        except ObjectDoesNotExist:
            Save(
                user = request.user,
                game = Game.objects.get(title=game_title),
                data = new_save
            ).save()
            return HttpResponse('Ok')
        except MultipleObjectsReturned:
            raise Http404('<h1>Multiple saves found. This should not happen.</h1>')
        except Exception:
            raise Http404("Could not find the required parameters.")

def load_game_state(request, version):
    if request.method == 'GET':
        try:
            game_title = request.GET.get('title')
            save = get_savedata(request.user, game_title)
            return JsonResponse(save.data, safe=False)
        except MultipleObjectsReturned:
            raise Http404('<h1>Multiple saves found.</h1>')
        except ObjectDoesNotExist:
            raise Http404('<h1>No save found.</h1>')
        except Exception:
            raise Http404('<h1>Unknown error loading game save.</h1>')

def own_game(request):
    return render(request, 'own_game/own_game.html', {})

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your LaTeLaTeGaMeS account!'
            message = render_to_string('activation_mail.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'activate.html', {})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def about(request):
    return render(request, 'about.html', {})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = StoreUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ObjectDoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'activation_confirmation.html', {'username': user.username})
    else:
        return render(request, 'activation_confirmation.html', {})
