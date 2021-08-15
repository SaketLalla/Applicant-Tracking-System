from django.shortcuts import render

# Create your views here.
def compare(request):
    jd = request.GET['jobdescription']
    list_jd = jd.split()
    skill ='python css java datahandling c++'
    list_skill = skill.split()
    list_skill.append('frontend')
    #print(list_skill)
    context={'jd':jd , 'count':len(list_jd) , 'skill_list':list_skill}
    return render(request , 'compare.html',context)