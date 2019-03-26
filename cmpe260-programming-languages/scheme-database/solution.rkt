#lang scheme
;2016402147

;3.0 - Some Helper Functions
;Helper functions returning the second,third and fourth elements of a given list.
(define SECOND (lambda(list) (car(cdr list))))
(define THIRD (lambda(list) (car(cdr(cdr list)))))
(define FOURTH (lambda(list) (car(cdr(cdr(cdr list))))))


; This is a helper function to be used in implementing 3.1 Simple Queries
; SEARCH takes 2 parameters, item database and order.
; item: item that is being searched.
; database: Which database we are searching at. For this example, it means LOCATIONS or TRAVELERS.
; order: What is the position of the element in the given list.
; Example call: (SEARCH 'newyork TRAVELERS SECOND)
; It returns the list of lists, which has the item in the given position(order).
(define SEARCH (lambda(item database order)
                 (cond ((equal? database '()) '())
                       ((equal? item (order(car database)))
                        (car database))
                       (else (SEARCH item (cdr database) order)))))


;This is a helper function for adding an element to a list.
; ex: (addToList (list 'newyork 'cali) 'erzurum) returns (newyork cali erzurum)
(define (addToList the_list element) 
  (if (null? the_list) 
      (list element)
      (cons (car the_list)
            (addToList (cdr the_list) element))))


;TASK 3.1 - Simple Queries

;This function uses SEARCH helper.
;It searches the given location, at the first positions of the LOCATIONS database.
; Then returns the third element of that list, which is list of railway connections.
; If the location is not present in the database, returns empty list.
(define RAILWAY-CONNECTION (lambda (location)
                             (if (equal? (SEARCH location LOCATIONS car) '())
                                 '() (THIRD (SEARCH location LOCATIONS car)))))

;This function also uses SEARCH helper.
;It searches the given location, at the first positions of the LOCATIONS database.
; Then returns the second element of that list, which is the accommodation cost.
; If the location is not present in the database, returns 0.
(define ACCOMMODATION-COST (lambda (location)
                             (if (equal? (SEARCH location LOCATIONS car) '()) 0
                                 ( SECOND(SEARCH location LOCATIONS car)))))


;INTERESTED-CITIES searches the given person, at the first positions of the TRAVELERS database.
; Then returns the second element of that list, which is the list of interested cities.
; If the person is not present in the database, returns empty list.
(define INTERESTED-CITIES (lambda (person)
                            (if (equal? (SEARCH person TRAVELERS car) '()) '()
                                ( SECOND(SEARCH person TRAVELERS car)))))


;INTERESTED-ACTIVITIES searches the given person, at the first positions of the TRAVELERS database.
; Then returns the third element of that list, which is the list of interested activities.
; If the person is not present in the database, returns empty list.
(define INTERESTED-ACTIVITIES (lambda (person)
                                (if (equal? (SEARCH person TRAVELERS car) '()) '()
                                    ( THIRD(SEARCH person TRAVELERS car)))))


;HOME  searches the given person, at the first positions of the TRAVELERS database.
; Then returns the fourth element of that list, which is the hometown of the person.
; If the person is not present in the database, returns empty list.
(define HOME (lambda (person)
               (if (equal? (SEARCH person TRAVELERS car) '()) '()
                   ( FOURTH(SEARCH person TRAVELERS car)))))

;TASK 3.2 - Constructing Lists

; FORMLIST is a helper function for the tasks of 3.2
; It has 5 parameters.
; item: The property we are looking for.
; database: Which database we are searching at. For this example, it means LOCATIONS or TRAVELERS.
; the_list: The list that we will return. This list will consist of the elements with the searched property(item).
; searched: Position of the property we are looking for. For a person if it is the name, it will be car, if it is the interested cities, it will be SECOND.
; order: The position of the elements that we will add to our list. If we are looking for names, we will add their position to here.
; Ex: (FORMLIST 'newyork TRAVELERS '() car FOURTH)
; This will return the list of the names of travelers who are from newyork. We are looking for names, so searched is car. We are looking for hometowns, so order is FOURTH.

(define FORMLIST (lambda(item database the_list searched order)
                   (cond ((equal? database '()) the_list)
                         ((not (member item
                                       (if (list?(order(car database)))
                                           (order(car database)) (list(order(car database))))))
                          (FORMLIST item (cdr database) the_list searched order))
                         (else(FORMLIST item (cdr database)
                                        (addToList the_list (searched(car database))) searched order) ))))



;TRAVELER-FROM uses FORMLIST to return list of names who are from the location.
(define TRAVELER-FROM (lambda (location)
                        (FORMLIST location TRAVELERS '() car FOURTH)))

;INTERESTED-IN-CITY uses FORMLIST to return list of names who are interested in visiting a given location.
(define INTERESTED-IN-CITY (lambda (location)
                             (FORMLIST location TRAVELERS '() car SECOND)))

;INTERESTED-IN-ACTIVITY uses FORMLIST to return list of names who are interested in a given activity.
(define INTERESTED-IN-ACTIVITY (lambda (activity)
                                 (FORMLIST activity TRAVELERS '() car THIRD)))

;TASK 3.3 - CONNECTED CITIES

;HELP-RAILWAY function is the helper function for RAILWAY-NETWORK.
;It consists of 3 parameters.
;City: The city that we are looking for its network.
;the-network: Current list of cities that are in the network.
;queue: List of cities that we will look for other cities from.
;This function works in the following way:
;If the queue is empty, we will return all the elements of the the-network except for the first one.
;This is to ensure we are not returning the starting city in the network.
;If it's not, we will look at the first element of queue.
;If we have not visited that city before, we will add it to our the-network, and its connections to queue.
;If we have visited that city, we will simply bypass this item and call the function with rest of the queue.
;This is basically a Breadth First Search Algorithm.

(define HELP_RAILWAY (lambda (city the-network queue)
                       (cond ((equal? queue '()) (cdr the-network))
                             ((not (member (car queue) the-network))
                              (HELP_RAILWAY city (addToList the-network (car queue))
                                            (append (cdr queue) (RAILWAY-CONNECTION (car queue)))))
                             (else(HELP_RAILWAY city the-network (cdr queue))))))

; RAILWAY-NETWORK initiates the HELP-RAILWAY function.
; It adds the current city to our network, and its connections to our queue.
(define RAILWAY-NETWORK (lambda (city)
                          (HELP_RAILWAY city (list city) (RAILWAY-CONNECTION city))))

;TASK 3.4 - EXPENSES

;A helper function that returns the activities in a city.
(define CITY-ACTIVITIES (lambda (location)
                          (if (equal? (SEARCH location LOCATIONS car) '())
                              '() (FOURTH (SEARCH location LOCATIONS car)))))

;A function that returns whether the given traveler is interested in one of the activities at a given location.
(define MATCHING-INTEREST (lambda (traveler location activities)
                            (cond
                              ((equal? activities '()) #f)
                              ((not (member (car activities) (CITY-ACTIVITIES location)))
                               (MATCHING-INTEREST traveler location (cdr activities)))
                              (else #t))))

;ACCOMODATION-EXPENSES function has 3 cases.
;If the location is travelers hometown, it return 0.
;Else if the MATCHING-INTEREST function returns true, it will mean that the traveler and location has a matching activity, then it will triple the expenses.
;Else it will return the accommodation cost of the location.

(define ACCOMMODATION-EXPENSES (lambda (traveler location)
                                 (cond
                                   ((eqv? location (HOME traveler)) 0)
                                   ((eqv? (MATCHING-INTEREST traveler location (INTERESTED-ACTIVITIES traveler)) #t)
                                    (* 3 (ACCOMMODATION-COST location)))
                                   (else (ACCOMMODATION-COST location)))))

;TRAVEL-EXPENSES function has 3 cases.
;If the location is travelers hometown, it return 0.
;Else if the location is not in the network of travelers' hometown, it will return 200, which will mean the transportation by plane.
;Else it will return 100, since it will be reachable by train.
(define TRAVEL-EXPENSES (lambda (traveler location)
                          (cond
                            ((eqv? location (HOME traveler)) 0)
                            ((not (member location (RAILWAY-NETWORK (HOME traveler)))) 200)
                            (else 100))))

;EXPENSES function basically sums the travel and accommodation expenses.
(define EXPENSES (lambda (traveler location)
                   (+ (TRAVEL-EXPENSES traveler location) (ACCOMMODATION-EXPENSES traveler location))))

;TASK 3.5 - CATEGORIZING CITIES

;This is a function with 4 parameters, for IN-BETWEEN function.
;lower: Lower bound of the interval.
;upper: Upper bound of the interval.
;in-range: List of cities that in the range we are looking for.
;cities: List of cities we will check the condition for.
(define HELP-IN-BETWEEN (lambda (lower upper in-range cities)
                          (cond
                            ((eqv? cities '()) in-range)
                            ((and (<= lower (SECOND(car cities))) (>= upper (SECOND(car cities))))
                             (HELP-IN-BETWEEN lower upper (addToList in-range (car(car cities))) (cdr cities)))
                            (else (HELP-IN-BETWEEN lower upper in-range (cdr cities))))))

;Initial call of HELP-IN-BETWEEN function is made with all the cities, and given bounds.                            
(define IN-BETWEEN (lambda (lower upper)
                     (HELP-IN-BETWEEN lower upper '() LOCATIONS)))

