#lang scheme

(define LOCATIONS
  '(
    (newyork 100 (ohio indiana newjersey) (theatre concert opera))
    (california 120 (washington utah) (theatre))
    (ohio 75 (newyork indiana newjersey) (concert))
    (moscow 95 () (concert opera))
    (paris 150 (nice cannes) (concert opera))
    (copenhagen 95 (nuenen) (theatre concert opera))
    (texas 80 (utah illinois indiana) (theatre concert))
    (cambridge 90 (cork london nuenen brussels) (theatre))
    (brussels 90 (london cambridge nuenen paris vienna) (theatre concert opera))
    (newjersey 100 (ohio newyork) (theatre concert))))

(define TRAVELERS
  '(
    (john (ohio texas) (theatre concert opera) newyork)
    (james (texas ohio copenhagen) (theatre concert opera) newjersey)
    (richard (cambridge ohio texas) (theatre concert) california)
    (alan (california ohio) () cambridge)
    (mary (california) (concert) cambridge)
    (ingrid (moscow ohio texas) (opera) brussels)))



