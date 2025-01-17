# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainingPlan, ExerciseSet, Exercise
from .forms import TrainingPlanForm, ExerciseSetForm
from django.views import View
from django.http import HttpResponse
from datetime import timedelta

# List all exercises
def exercise_list(request):
    exercises = Exercise.objects.all()
    print("exercises") # This will print the exercises in the console
    return render(request, 'exercise/list.html', {'exercises': exercises})

# Add new exercise
def exercise_add(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        category = request.POST['category']
        muscles_targeted = request.POST['muscles_targeted']
        Exercise.objects.create(name=name, description=description, category=category, muscles_targeted=muscles_targeted)
        return redirect('exercise_list')
    return render(request, 'exercise/add.html')

# Edit existing exercise
def exercise_edit(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise.name = request.POST['name']
        exercise.description = request.POST['description']
        exercise.category = request.POST['category']
        exercise.muscles_targeted = request.POST['muscles_targeted']
        exercise.save()
        return redirect('exercise_list')
    return render(request, 'exercise/edit.html', {'exercise': exercise})

# Delete exercise
def exercise_delete(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise.delete()
        return redirect('exercise_list')
    return render(request, 'exercise/delete.html', {'exercise': exercise})

# Training Plan CRUD
def training_plan_list(request):
    plans = TrainingPlan.objects.filter(user=request.user)
    return render(request, 'training_plan/training_plan_list.html', {'plans': plans})

def training_plan_add(request):
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST)
        if form.is_valid():
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()
            return redirect('training_plan_list')
    else:
        form = TrainingPlanForm()
    return render(request, 'training_plan/training_plan_add.html', {'form': form})


def training_plan_edit(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    
    if request.method == "POST":
        form = TrainingPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()  # Save the main form instance
            
            # Process exercise sets
            for exercise_set in plan.exercise_sets.all():
                sets = request.POST.get(f'sets_{exercise_set.id}')
                repetitions = request.POST.get(f'repetitions_{exercise_set.id}')
                rest_time = request.POST.get(f'rest_time_{exercise_set.id}')

                # Debug output to see received values
                print(f"ID: {exercise_set.id}, Sets: {sets}, Repetitions: {repetitions}, Rest Time: {rest_time}")

                if sets and repetitions and rest_time:  # Ensure all fields are present
                    try:
                        exercise_set.sets = int(sets)
                        exercise_set.repetitions = int(repetitions)
                        # Convert rest_time from seconds to timedelta
                        exercise_set.rest_time = timedelta(seconds=int(rest_time))
                        exercise_set.save()
                    except ValueError as ve:
                        print(f"Value error for ExerciseSet ID {exercise_set.id}: {ve}")
                else:
                    print(f"Error: Missing data for ExerciseSet ID {exercise_set.id}")

            return redirect('training_plan_detail', plan_id=plan.id)

    else:
        form = TrainingPlanForm(instance=plan)

    return render(request, 'training_plan/training_plan_edit.html', {'form': form, 'plan': plan})


def training_plan_delete(request, id):  # Changed 'plan_id' to 'id'
    plan = get_object_or_404(TrainingPlan, id=id)
    if request.method == 'POST':
        plan.delete()
        return redirect('training_plan_list')
    return render(request, 'training_plan/training_plan_delete.html', {'plan': plan})

# Exercise Set CRUD
def exercise_set_add(request, training_plan_id):
    training_plan = get_object_or_404(TrainingPlan, id=training_plan_id)
    if request.method == 'POST':
        form = ExerciseSetForm(request.POST)
        if form.is_valid():
            exercise_set = form.save(commit=False)
            exercise_set.training_plan = training_plan  # Link to the training plan
            exercise_set.save()  # Save the exercise set
            return redirect('training_plan_edit', plan_id=training_plan.id)  # Correct redirection
    else:
        form = ExerciseSetForm()
    return render(request, 'exercise_set/exercise_set_add.html', {'form': form, 'training_plan': training_plan})


def training_plan_detail(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    return render(request, 'training_plan/training_plan_detail.html', {'plan': plan})


def exercise_set_edit(request, id):
    exercise_set = get_object_or_404(ExerciseSet, id=id)
    if request.method == 'POST':
        form = ExerciseSetForm(request.POST, instance=exercise_set)
        if form.is_valid():
            form.save()
            return redirect('training_plan/training_plan_edit', id=exercise_set.training_plan.id)
    else:
        form = ExerciseSetForm(instance=exercise_set)
    return render(request, 'exercise_set/exercise_set_edit.html', {'form': form, 'set': exercise_set})


def exercise_set_delete(request, id):
    exercise_set = get_object_or_404(ExerciseSet, id=id)
    training_plan_id = exercise_set.training_plan.id
    if request.method == 'POST':
        exercise_set.delete()
        return redirect('training_plan/training_plan_edit', id=training_plan_id)
    return render(request, 'exercise_set/exercise_set_confirm_delete.html', {'exercise_set': exercise_set})

def home(request):
    return render(request, 'base_template/home.html')