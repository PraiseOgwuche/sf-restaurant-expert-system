% Tell prolog that known/3 and multivalued/1 will be added later
:- dynamic known/3, multivalued/1.

% Define multivalued predicates
multivalued(meal_type).
multivalued(diet).
multivalued(group_size).

% Restaurant recommendations based on preferences
restaurant(raavi):- location(san_francisco), meal_type(lunch), diet(halal), cuisine(indian), price(affordable), distance(walking_distance), atmosphere(casual), service_style(dine_in), (group_size(small_group); group_size(solo)), noise(moderate).

restaurant(red_chilli):- location(san_francisco), meal_type(lunch), diet(halal), cuisine(indian), price(moderate), distance(muni_required), atmosphere(casual), service_style(dine_in), (group_size(small_group); group_size(solo)), noise(moderate).

restaurant(kin_khao):- location(san_francisco), meal_type(lunch), diet(standard), cuisine(thai), price(moderate), distance(walking_distance), atmosphere(trendy), service_style(dine_in), (group_size(large_group); group_size(small_group); group_size(solo)), noise(lively).

restaurant(sababa):- location(san_francisco), (meal_type(lunch); meal_type(dinner)), (diet(halal); diet(vegetarian)), cuisine(middle_eastern), price(moderate), distance(muni_required), atmosphere(casual), service_style(dine_in), (group_size(small_group); group_size(large_group); group_size(solo)), noise(moderate).

restaurant(tratto):- location(san_francisco), meal_type(breakfast), diet(vegetarian), cuisine(italian), price(expensive), distance(walking_distance), atmosphere(upscale), service_style(dine_in), (group_size(small_group); group_size(solo)), noise(quiet).

restaurant(taylor_street_coffee):- location(san_francisco), meal_type(breakfast), diet(standard), cuisine(american), price(moderate), distance(walking_distance), atmosphere(cozy), service_style(dine_in), (group_size(small_group); group_size(solo)), noise(moderate).

restaurant(mr_charlies):- location(san_francisco), (meal_type(lunch); meal_type(dinner)), diet(vegan), cuisine(american), price(affordable), distance(walking_distance), atmosphere(casual), service_style(quick_bite), group_size(solo), noise(lively).

restaurant(grove_yerba_buena):- location(san_francisco), (meal_type(breakfast); meal_type(lunch)), diet(vegetarian), cuisine(american), price(moderate), distance(walking_distance), atmosphere(cozy), service_style(dine_in), (group_size(small_group); group_size(solo)), noise(moderate).

restaurant(mkt_restaurant):- location(san_francisco), (meal_type(breakfast); meal_type(lunch); meal_type(dinner)), diet(standard), cuisine(american), price(expensive), distance(walking_distance), atmosphere(upscale), service_style(dine_in), (group_size(small_group); group_size(solo)), noise(quiet).

restaurant(brendas_french_soul):- location(san_francisco), (meal_type(breakfast); meal_type(lunch)), diet(standard), cuisine(american), price(moderate), distance(bart_required), atmosphere(casual), service_style(dine_in), (group_size(small_group); group_size(solo)), noise(lively).

restaurant(thats_my_jam):- location(san_francisco), (meal_type(breakfast); meal_type(lunch)), diet(standard), cuisine(american), price(affordable), distance(walking_distance), atmosphere(casual), service_style(quick_bite), group_size(solo), noise(moderate).

restaurant(subway):- location(san_francisco), (meal_type(lunch); meal_type(dinner)), (diet(vegetarian); diet(vegan)), cuisine(american), price(affordable), distance(walking_distance), atmosphere(casual), service_style(quick_bite), group_size(solo), noise(quiet).

restaurant(gotts_roadside):- location(san_francisco), (meal_type(lunch); meal_type(dinner)), diet(standard), cuisine(american), price(moderate), distance(muni_required), atmosphere(casual), service_style(quick_bite), (group_size(small_group); group_size(solo)), noise(lively).

restaurant(burger_king):- location(san_francisco), (meal_type(breakfast); meal_type(lunch); meal_type(dinner)), diet(standard), cuisine(american), price(affordable), distance(walking_distance), atmosphere(casual), service_style(quick_bite), (group_size(solo); group_size(small_group); group_size(large_group)), noise(moderate).

restaurant(mcdonalds):- location(san_francisco), (meal_type(breakfast); meal_type(lunch); meal_type(dinner)), diet(standard), cuisine(american), price(affordable), distance(walking_distance), atmosphere(casual), service_style(quick_bite), (group_size(solo); group_size(small_group); group_size(large_group)), noise(moderate).

restaurant(in_n_out):- location(san_francisco), (meal_type(lunch); meal_type(dinner)), diet(standard), cuisine(american), price(affordable), distance(bart_required), atmosphere(casual), service_style(quick_bite), (group_size(solo); group_size(small_group); group_size(large_group)), noise(lively).

restaurant(scomas):- location(san_francisco), (meal_type(lunch); meal_type(dinner)), diet(standard), cuisine(seafood), price(expensive), distance(bart_required), atmosphere(upscale), service_style(dine_in), (group_size(small_group); group_size(solo)), noise(moderate).

restaurant(hinodeya_ramen):- location(san_francisco), (meal_type(lunch); meal_type(dinner)), diet(standard), cuisine(japanese), price(moderate), distance(bart_required), atmosphere(casual), service_style(dine_in), (group_size(small_group); group_size(solo)), noise(moderate).

restaurant(panda_express):- location(san_francisco), (meal_type(lunch); meal_type(dinner)), diet(standard), cuisine(chinese), price(affordable), distance(muni_required), atmosphere(casual), service_style(quick_bite), (group_size(solo); group_size(small_group)), noise(moderate).

% This checks if the user is not in San Francisco
restaurant(ask_others):- \+location(san_francisco).

% Define the location rule
location(X) :- ask(location, X).

% Define the meal_type rule with natural language
meal_type(X) :- menuask("What meal are you looking for?", X, [breakfast, lunch, dinner]).

% Define the cuisine rule with natural language
cuisine(X) :- menuask("What kind of food are you in the mood for today?", X, [american, chinese, italian, japanese, mexican, thai, indian, middle_eastern, seafood]).

% Define the diet rule with natural language
diet(X) :- menuask("Do you have any specific dietary requirements or preferences?", X, [standard, vegetarian, vegan, halal, gluten_free]).

% Define the price rule with natural language
price(X) :- menuask("What price range are you comfortable with for this meal?", X, [affordable, moderate, expensive]).

% Define the distance rule with natural language
distance(X) :- menuask("How far are you willing to travel from Minerva residence?", X, [walking_distance, muni_required, bart_required]).

% Define the atmosphere rule with natural language
atmosphere(X) :- menuask("What kind of dining atmosphere would you prefer?", X, [casual, upscale, cozy, trendy, quiet]).

% Define the service_style rule with natural language
service_style(X) :- menuask("What type of service are you looking for?", X, [dine_in, take_out, quick_bite]).

% Define the group_size rule with natural language
group_size(X) :- menuask("How many people will be dining?", X, [solo, small_group, large_group]).

% Define the noise rule with natural language
noise(X) :- menuask("What noise level would be ideal for your dining experience?", X, [quiet, moderate, lively]).

% Asking clauses
ask(A, V):-
    known(yes, A, V), % succeed if true
    !.  % stop looking

ask(A, V):-
    known(_, A, V), % fail if false
    !, fail.

% If not multivalued, and already known, do not ask again for a different value.
ask(A, V):-
    \+multivalued(A),
    known(yes, A, V2),
    V \== V2,
    !.

ask(A, V):-
    read_py(A,V,Y), % get the answer
    assertz(known(Y, A, V)), % remember it
    Y == yes.    % succeed or fail

% Reference: http://www.amzi.com/ExpertSystemsInProlog/02usingprolog.php

menuask(A, V, _):-
    known(yes, A, V), % succeed if true
    !.  % stop looking

menuask(A, V, _):-
    known(yes, A, V2), % If already known, do not ask again for a different value
    V \== V2,
    !, fail.

menuask(A, V, Menu):-
    read_menu_py(A,X,Menu),
    confirm_answer(X,A,V,Menu),
    asserta(known(yes,A,X)),
    X == V.

confirm_answer(X,_,_,Menu):-
    member(X,Menu),
    !.
confirm_answer(X,A,V,Menu):-
    dialog_response(X), dialog_response(" Please, change your input.\n"),
    menuask(A, V, Menu).

    