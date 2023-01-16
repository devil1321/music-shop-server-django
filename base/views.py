import base64, os
import json
import re
import stripe
from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import Price, Track,Person
from django.core import serializers
# Create your views here.
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class HomeView(APIView):
    permission_classes = ()
    template_name = "index.html"
    def get(self, request, *args, **kwargs):
        return render(self.request,self.template_name)

class InitView(APIView):
    permission_classes = (IsAuthenticated,)
    template_name = "home.html"
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return JsonResponse(serializers.serialize('json', [self.request.user]), safe=False)
        else:
            return JsonResponse({'msg':'You`re not logged in.'})

class InitPersonView(APIView):
    permission_classes = (IsAuthenticated,)
    template_name = "home.html"
    model = Person
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            person  = self.model.objects.get(pk=self.request.user.id)
            return JsonResponse(serializers.serialize('json', [person]), safe=False)
        else:
            return JsonResponse({'msg':'You`re not logged in.'})

class FileView(APIView):
     template_name=""
     model = Track
     permission_classes = (IsAuthenticated,)
     def post(self, request, *args, **kwargs):
         body = json.loads(request.body) 
         if self.request.user:
            for file in os.listdir(os.path.join(os.getcwd(),"media")):
               if file == body["params"]['name']:
                   name = body["params"]['name']
                   with open(os.path.join(os.getcwd(),"media/" + name), "rb") as music_file:
                       encoded_string = base64.b64encode(music_file.read()).decode('utf-8')
                       string = f'media/{file}'.format(file=file)
                       string = re.sub(r' ',"_",string)
                       track = self.model.objects.filter(file=string)
                       if track.exists():
                            encoded_image = base64.b64encode(track[0].image.file.read()).decode('utf-8')
                            fileData = {
                                "id":track[0].id,
                                "base64":'data:audio/mpeg;base64,' + encoded_string,
                                "image":'data:image/jpeg;base64,' + encoded_image,
                                'title':track[0].title,
                                'author':track[0].author,
                                'genres':track[0].genres,
                                'tags':track[0].tags,
                            }
                            return JsonResponse({"file":fileData})  
                       else:
                            return JsonResponse({"msg":'Track not exists'})  
         else:
             return JsonResponse({"msg":"file not found"})
 
class FilesView(APIView):
    template_name=""
    model = Track
    permission_classes = (IsAuthenticated,)
    
    def get(self,request,*args,**kwargs):
        if self.request.user:           
            files = []
            for file in os.listdir(os.path.join(os.getcwd(),"media")):
                 with open(os.path.join(os.getcwd(),"media/" + file), "rb") as music_file:
                       encoded_string = base64.b64encode(music_file.read()).decode('utf-8')
                       string = f'media/{file}'.format(file=file)
                       string = re.sub(r' ',"_",string)
                       track = self.model.objects.filter(file=string)
                       if track.exists():
                            encoded_image = base64.b64encode(track[0].image.file.read()).decode('utf-8')
                            fileData = {
                                'id':track[0].id,
                                "base64":'data:audio/mpeg;base64,' + encoded_string,
                                "image":'data:image/jpeg;base64,' + encoded_image,
                                'title':track[0].title,
                                'author':track[0].author,
                                'genres':track[0].genres,
                                'tags':track[0].tags,
                            }
                            files.append(fileData)         
            return JsonResponse({"files":files})  
        else:
            return JsonResponse({"msf":'signin or login firts'})  
                      
     
class AddTrackView(APIView):
    template_name = 'manage-tracks.html'
    model = Track
    permission_classes = (IsAuthenticated,)
    
    def post(self,request,*args,**kwargs):
        file = self.request.FILES.get('file')
        image = self.request.FILES.get('image')
        title = self.request.POST.get('title')
        author = self.request.POST.get('author')
        tags = self.request.POST.get('tags')
        genres = self.request.POST.get('genres')
        price = self.request.POST.get('price')
        price_id = self.request.POST.get('price_id')
        
        if self.request.user.is_staff:
            if self.model.objects.filter(title=title).exists():
                return JsonResponse({'msg':"Track is arleady on list"})
            else:
                modelToSave = self.model.objects.create(file=file,image=image,title=title,author=author,tags=tags,genres=genres,price=price,price_id=price_id)
                try:
                    modelToSave.save()
                    return JsonResponse({"msg":"Track added"})
                except:
                    return JsonResponse({'msg':'Fill all fields'})
        else:
            return JsonResponse({'msg':'You`re not allowed'})

             
class UpdateTrackView(APIView):
    template_name = 'manage-tracks.html'
    model = Track
    permission_classes = (IsAuthenticated,)
    
    def post(self,request,*args,**kwargs):
        if self.request.user.is_staff:
            id = self.request.POST.get('id')
            file = self.request.FILES.get('file')
            image = self.request.FILES.get('image')
            title = self.request.POST.get('title')
            author = self.request.POST.get('author')
            tags = self.request.POST.get('tags')
            genres = self.request.POST.get('genres')
            price = self.request.POST.get('price')
            price_id = self.request.POST.get('price_id')
            track = self.model.objects.get(id=id)
            track.file = file
            track.image = image
            track.title = title
            track.author = author
            track.tags = tags
            track.genres = genres
            track.price = price
            track.price_id = price_id
            try:
                track.save()
                return JsonResponse({"msg":"Track Updated"})
            except:
                return JsonResponse({'msg':'Track Not Updated'})
        else:
            return JsonResponse({'msg':'You`re not allowed'})
 
class DeleteTrackView(APIView):
    template_name = 'manage-tracks.html'
    model = Track
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        if self.request.user.is_staff:
            track = self.model.objects.get(id=kwargs["id"])
            track.delete()
            return JsonResponse({"msg":"Track Deleted"})
        else:
            return JsonResponse({'msg':'You`re not allowed'})
 
class RegisterView(APIView):
    authentication_classes = [] #disables authentication
    permission_classes = [] #disables perm
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return redirect('home',{'user':self.request.user})



class CreateCheckoutSessionView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        cart = json.loads(self.request.body)
        if settings.DEBUG:
            domain = "http://localhost:8000"
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items = cart,
                mode='payment',
                success_url=domain + '/success/',
                cancel_url=domain + '/cancel/',
            )
        return redirect(checkout_session.url)



    
def Custom500View(request, *args, **argv):
    return render(request,'500.html',{"user":request.user},status=500)
   
def Custom404View(request, *args, **argv):
    return render(request,'404.html',{"user":request.user},status=404)
   


   
        