#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "hcq.h"
#define INPUT_BUFFER_SIZE 256

void *
Malloc (int size)
{
  void *result = malloc (size);
  if (result == NULL)
    {
      perror ("Malloc error");
      exit (1);
    }
  return result;
}

/*
 * Return a pointer to the struct student with name stu_name
 * or NULL if no student with this name exists in the stu_list
 */
Student *
find_student (Student * stu_list, char *student_name)
{
  Student *current = stu_list;
  while (current != NULL)
    {
      if (strcmp (current->name, student_name) == 0)
    {
      return current;
    }
      else
    {
      current = current->next_overall;
    }
    }
  return NULL;
}



/*   Return a pointer to the ta with name ta_name or NULL
 *   if no such TA exists in ta_list. 
 */
Ta *
find_ta (Ta * ta_list, char *ta_name)
{
  Ta *head = ta_list;
  while (head != NULL)
    {
      if (strcmp (head->name, ta_name) == 0)
    {
      return head;
    }
      head = head->next;
    }
  return NULL;
}


/*  Return a pointer to the course with this code in the course list
 *  or NULL if there is no course in the list with this code.
 */
Course *
find_course (Course * courses, int num_courses, char *course_code)
{
  for (int i = 0; i < num_courses; i++)
    {
      if (strcmp ((courses + i)->code, course_code) == 0)
    {
      return (courses + i);
    }
    }
  return NULL;
}


//This is the helper function for take_next_overall/course functions.

void
remove_from_queue (Student ** stu_list_ptr, Student * toRemove)
{
  Student *head = *stu_list_ptr;
  //if the student is the head, just remove the head
  //and make the next student the head.
  if (head == toRemove)
    {
      *stu_list_ptr = toRemove->next_overall;
    }
  else
    {
      //else, we need to keep the previous node as well, to connect
      //it to the next node.
      while (head->next_overall != toRemove)
    {
      head = head->next_overall;
    }
      head->next_overall = toRemove->next_overall;
    }
  //If a student is coming from the queue, she/he should be the
  //head of its course.
  toRemove->course->head = toRemove->next_course;
  if (toRemove->course->tail == toRemove)
    {
      toRemove->course->tail = NULL;
    }
  toRemove->course->wait_time +=
    difftime (time (0), *(toRemove->arrival_time));
  *(toRemove->arrival_time) = time (0);
}

/* Add a student to the queue with student_name and a question about course_code.
 * if a student with this name already has a question in the queue (for any
   course), return 1 and do not create the student.
 * If course_code does not exist in the list, return 2 and do not create
 * the student struct.
 * For the purposes of this assignment, don't check anything about the 
 * uniqueness of the name. 
 */
int
add_student (Student ** stu_list_ptr, char *student_name, char *course_code,
         Course * course_array, int num_courses)
{
  Student *current = find_student (*stu_list_ptr, student_name);
  //condition 1
  if (current != NULL)
    {
      return 1;
    }
  Course *ccourse = find_course (course_array, num_courses, course_code);
  //condition 2
  if (ccourse == NULL)
    {
      return 2;
    }
  //allocate memory for student and its fields.
  current = Malloc (sizeof (Student));
  current->name = Malloc (sizeof (char) * (strlen (student_name) + 1));
  strncpy (current->name, student_name, strlen (student_name));
  current->name[strlen (student_name)] = '\0';
  current->course = ccourse;
  current->arrival_time = Malloc (sizeof (time_t));
  *(current->arrival_time) = time (0);
  current->next_overall = NULL;
  current->next_course = NULL;

  //Start looking for the end of the queue.
  Student *prev = *stu_list_ptr;
  Student *prevc = ccourse->head;
  //if no students in the queue, make her/him the head.
  if (prev == NULL)
    {
      *stu_list_ptr = current;
    }
  else
    {
      while (prev != NULL)
    {
      if (prev->next_overall == NULL)
        break;
      prev = prev->next_overall;
    }
      prev->next_overall = current;
    }

  //now add the student to the course specific queue.
  if (prevc == NULL)
    {
      ccourse->head = current;
      ccourse->tail = current;
    }
  else
    {
      ccourse->tail->next_course = current;
      ccourse->tail = current;
    }
  return 0;
}


/* Student student_name has given up waiting and left the help centre
 * before being called by a Ta. Record the appropriate statistics, remove
 * the student from the queues and clean up any no-longer-needed memory.
 *
 * If there is no student by this name in the stu_list, return 1.
 */
int
give_up_waiting (Student ** stu_list_ptr, char *student_name)
{
  Student *givup = find_student (*stu_list_ptr, student_name);
  Student *head = *stu_list_ptr;
  if (givup == NULL)
    {
      return 1;
    }
  Student *chead = givup->course->head;

  //check if the givenup student is head.
  //if not, look for her/him in the queue.
  if (head == givup)
    {
      *stu_list_ptr = givup->next_overall;
    }
  else
    {
      while (head != NULL)
    {
      if (head->next_overall == givup)
        {
          head->next_overall = givup->next_overall;
          break;
        }
      head = head->next_overall;
    }
    }
  //now do the same for the course queue
  if (chead == givup)
    {
      givup->course->head = givup->next_course;
      if (givup == givup->course->tail)
    {
      givup->course->tail = givup->next_course;
    }
    }
  else
    {
      while (chead != NULL)
    {
      if (chead->next_course == givup)
        {
          chead->next_course = givup->next_course;
          break;
        }
      chead = chead->next_course;
    }
    }

  givup->course->bailed += 1;
  time_t now = time (0);
  givup->course->wait_time += difftime (now, *(givup->arrival_time));
  free (givup->name);
  free (givup->arrival_time);
  free (givup);
  return 0;
}

/* Create and prepend Ta with ta_name to the head of ta_list. 
 * For the purposes of this assignment, assume that ta_name is unique
 * to the help centre and don't check it.
 */
void
add_ta (Ta ** ta_list_ptr, char *ta_name)
{
  // first create the new Ta struct and populate
  Ta *new_ta = Malloc (sizeof (Ta));
  new_ta->name = Malloc (strlen (ta_name) + 1);
  strcpy (new_ta->name, ta_name);
  new_ta->current_student = NULL;

  // insert into front of list
  new_ta->next = *ta_list_ptr;
  *ta_list_ptr = new_ta;
}

/* The TA ta is done with their current student. 
 * Calculate the stats (the times etc.) and then 
 * free the memory for the student. 
 * If the TA has no current student, do nothing.
 */
void
release_current_student (Ta * ta)
{
  if (ta->current_student != NULL)
    {
      time_t now = time (0);
      ta->current_student->course->helped += 1;
      ta->current_student->course->help_time +=
    difftime (now, *(ta->current_student->arrival_time));
      free (ta->current_student->name);
      free (ta->current_student->arrival_time);
      free (ta->current_student);
    }
}

/* Remove this Ta from the ta_list and free the associated memory with
 * both the Ta we are removing and the current student (if any).
 * Return 0 on success or 1 if this ta_name is not found in the list
 */
int
remove_ta (Ta ** ta_list_ptr, char *ta_name)
{
  Ta *head = *ta_list_ptr;
  if (head == NULL)
    {
      return 1;
    }
  else if (strcmp (head->name, ta_name) == 0)
    {
      // TA is at the head so special case
      *ta_list_ptr = head->next;
      release_current_student (head);
      // memory for the student has been freed. Now free memory for the TA.
      free (head->name);
      free (head);
      return 0;
    }
  while (head->next != NULL)
    {
      if (strcmp (head->next->name, ta_name) == 0)
    {
      Ta *ta_tofree = head->next;
      //  We have found the ta to remove, but before we do that 
      //  we need to finish with the student and free the student.
      //  You need to complete this helper function
      release_current_student (ta_tofree);

      head->next = head->next->next;
      // memory for the student has been freed. Now free memory for the TA.
      free (ta_tofree->name);
      free (ta_tofree);
      return 0;
    }
      head = head->next;
    }
  // if we reach here, the ta_name was not in the list
  return 1;
}


/* TA ta_name is finished with the student they are currently helping (if any)
 * and are assigned to the next student in the full queue. 
 * If the queue is empty, then TA ta_name simply finishes with the student 
 * they are currently helping, records appropriate statistics, 
 * and sets current_student for this TA to NULL.
 * If ta_name is not in ta_list, return 1 and do nothing.
 */
int
take_next_overall (char *ta_name, Ta * ta_list, Student ** stu_list_ptr)
{
  Ta *next = find_ta (ta_list, ta_name);
  if (next == NULL)
    {
      return 1;
    }
  release_current_student (next);
  if (*stu_list_ptr == NULL)
    {
      next->current_student = NULL;
    }
  else
    {
      next->current_student = *stu_list_ptr;
      remove_from_queue (stu_list_ptr, *stu_list_ptr);
    }

  return 0;
}



/* TA ta_name is finished with the student they are currently helping (if any)
 * and are assigned to the next student in the course with this course_code. 
 * If no student is waiting for this course, then TA ta_name simply finishes 
 * with the student they are currently helping, records appropriate statistics,
 * and sets current_student for this TA to NULL.
 * If ta_name is not in ta_list, return 1 and do nothing.
 * If course is invalid return 2, but finish with any current student. 
 */
int
take_next_course (char *ta_name, Ta * ta_list, Student ** stu_list_ptr,
          char *course_code, Course * courses, int num_courses)
{
  Ta *next = find_ta (ta_list, ta_name);
  Course *ccourse = find_course (courses, num_courses, course_code);
  if (next == NULL)
    {
      return 1;
    }
  release_current_student (next);
  if (ccourse == NULL)
    {
      return 2;
    }
  if (ccourse->head == NULL)
    {
      next->current_student = NULL;
    }
  else
    {
      next->current_student = ccourse->head;
      remove_from_queue (stu_list_ptr, ccourse->head);
    }
  return 0;
}


/* For each course (in the same order as in the config file), print
 * the <course code>: <number of students waiting> "in queue\n" followed by
 * one line per student waiting with the format "\t%s\n" (tab name newline)
 * Uncomment and use the printf statements below. Only change the variable
 * names.
 */
void
print_all_queues (Student * stu_list, Course * courses, int num_courses)
{
  int count = 0;
  for (int i = 0; i < num_courses; i++)
    {
      count = 0;
      Student *head = (courses + i)->head;
      while (head != NULL)
    {
      count += 1;
      head = head->next_course;
    }
      printf ("%s: %d in queue\n", (courses + i)->code, count);
      head = (courses + i)->head;
      while (head != NULL)
    {
      printf ("\t%s\n", head->name);
      head = head->next_course;
    }
    }
}


/*
 * Print to stdout, a list of each TA, who they are serving at from what course
 * Uncomment and use the printf statements 
 */
void
print_currently_serving (Ta * ta_list)
{
  Ta *head = ta_list;
  if (head == NULL)
    {
      printf ("No TAs are in the help centre.\n");
    }
  while (head != NULL)
    {
      if (head->current_student == NULL)
    {
      printf ("TA: %s has no student\n", head->name);
    }
      else
    {
      printf ("TA: %s is serving %s from %s\n", head->name,
          head->current_student->name,
          head->current_student->course->code);
    }
      head = head->next;
    }
}


/*  list all students in queue (for testing and debugging)
 *   maybe suggest it is useful for debugging but not included in marking? 
 */
void
print_full_queue (Student * stu_list)
{
  Student *head = stu_list;
  while (head != NULL)
    {
      printf ("%s %s %f\n", head->name, head->course->code,
          difftime (time (0), *(head->arrival_time)));
      head = head->next_overall;
    }
}

/* Prints statistics to stdout for course with this course_code
 * See example output from assignment handout for formatting.
 *
 */
int
stats_by_course (Student * stu_list, char *course_code, Course * courses,
         int num_courses, Ta * ta_list)
{

  // TODO: students will complete these next pieces but not all of this 
  //       function since we want to provide the formatting

  int students_waiting = 0, students_being_helped = 0;
  Course *found = find_course (courses, num_courses, course_code);
  if (found == NULL)
    {
      return 1;
    }
  Student *current = stu_list;
  Student *head = found->head;
  Ta *current_ta = ta_list;
  while (head != NULL)
    {
      students_waiting += 1;
      head = head->next_course;
    }
  while (current_ta != NULL)
    {
      if (found == NULL)
    {
      break;
    }
      current = current_ta->current_student;
      if (current != NULL && strcmp (current->course->code, course_code) == 0)
    {
      students_being_helped += 1;
    }
      current_ta = current_ta->next;
    }

  // You MUST not change the following statements or your code 
  //  will fail the testing. 

  printf ("%s:%s \n", found->code, found->description);
  printf ("\t%d: waiting\n", students_waiting);
  printf ("\t%d: being helped currently\n", students_being_helped);
  printf ("\t%d: already helped\n", found->helped);
  printf ("\t%d: gave_up\n", found->bailed);
  printf ("\t%f: total time waiting\n", found->wait_time);
  printf ("\t%f: total time helping\n", found->help_time);

  return 0;
}


/* Dynamically allocate space for the array course list and populate it
 * according to information in the configuration file config_filename
 * Return the number of courses in the array.
 * If the configuration file can not be opened, call perror() and exit.
 */
int
config_course_list (Course ** courselist_ptr, char *config_filename)
{
  FILE *my_file = fopen (config_filename, "r");
  if (my_file == NULL)
    {
      perror ("Error opening file/n");
      return 1;
    }
  char buf[INPUT_BUFFER_SIZE], course_code[7], desc[INPUT_BUFFER_SIZE - 7];
  fgets (buf, INPUT_BUFFER_SIZE, my_file);
  int length = strtol (buf, NULL, 10);
  *courselist_ptr = Malloc (length * sizeof (Course));
  for (int i = 0; i < length; i++)
    {
      fgets (buf, INPUT_BUFFER_SIZE, my_file);
      sscanf (buf, "%s %[^\n]", course_code, desc);
      strcpy ((*courselist_ptr + i)->code, course_code);
      (*courselist_ptr + i)->head = NULL;
      (*courselist_ptr + i)->tail = NULL;
      (*courselist_ptr + i)->helped = 0;
      (*courselist_ptr + i)->bailed = 0;
      (*courselist_ptr + i)->wait_time = 0;
      (*courselist_ptr + i)->help_time = 0;
      (*courselist_ptr + i)->description =
    Malloc ((strlen (desc) + 1) * sizeof (char));
      strncpy ((*courselist_ptr + i)->description, desc, strlen (desc));
      (*courselist_ptr + i)->description[strlen (desc)] = '\0';
    }
  return length;
}
