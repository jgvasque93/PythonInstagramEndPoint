from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import sys
import random
user = 'user'
pwd = 'password'

def commentsByHashtag(ListHashtag,fechatest,user,pwd):
    #login en el Api de instagram
    API = InstagramAPI(user,pwd)
    #print('login:',user,pwd)
    API.login()
    #fecha tope de extracion, se le cambio el formato
    dtfechaTest=datetime.strptime(fechatest, "%Y-%m-%d")
    fechaTest=dtfechaTest.strftime("%Y-%m-%d")
    #for para la lista de hashtags
    for hashtag in ListHashtag:
        try:
            #token id para busqueda, al inicio es vacio
            next_max_id = ''
            oportunity=0
            oppkIgual=20
            #coneccion a API para obtener post de los hashtags
            g = API.getHashtagFeed(hashtag,next_max_id)
            #temp obtiene la respuesta
            temp = API.LastJson
            # usamos un while para recorrer todas las paginas hasta llegar a la fecha tpe
            contadorLikes=0
            while 1:
                try:
                    oportunity=0
                    # g nos indica si hubo un error en el API al hacer la consulta
                    while g==False:
                        #esperamos un tiempo entre 150 y 270 segundos para volver a consultar
                        n = random.randint(50,90)
                        time.sleep(3*n)
                        g = API.getHashtagFeed(hashtag,next_max_id)
                        temp = API.LastJson
                    #recorremos nyestro json respuesta
                    salir=0
                    for item in temp["items"]:
                        #obtenemos el id del post y se lo mandamos a la funcion like() y comment del Api
                        # ademas escogemos al azar uno de nuestros comentarios
                        lc=random.choice(listaComments)
                        rp=API.like(item['id'])
                        rp=API.comment(item['id'],lc)
                        if(rp):
                            contadorLikes=contadorLikes+1
                        print('likes para hashtag:',hashtag,contadorLikes,item['code'])
                        #esperamos 50 segundos para no excder el limite de likes de instagram de 100 por hora
                        time.sleep(30)
                        #obtenemos la fecha y la comparamos con la fecha de corte 
                        ts=int(item['taken_at'])
                        fecha=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                        dtfechaD=datetime.strptime(fecha.split(' ')[0], "%Y-%m-%d")
                        fechaFinal=dtfechaD.strftime("%Y-%m-%d")
                        if(fechaFinal<fechatest):
                            #Muchas veces vienen post con otras fechas , asi que dejamos pasar 16 post hasta estar seguros que la fecha fue sobrepasada
                            if(oportunity<16):
                                oportunity=oportunity+1
                            else:
                                salir=1
                        if(salir==1):
                            break
                    try:
                        #repetimos el proceso de arriba pero para los hashtags populares que nos devuelve el api
                        for item in temp["ranked_items"]:
                            lc=random.choice(listaComments)
                            rp=API.like(item['id'])
                            rp=API.comment(item['id'],lc)                            
                            if(rp):
                                contadorLikes=contadorLikes+1
                            print('commnets para hashtag:',hashtag,contadorLikes,item['code'])
                            time.sleep(30)
                            ts=int(item['taken_at'])
                            fecha=datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                            dtfechaD=datetime.strptime(fecha.split(' ')[0], "%Y-%m-%d")
                            fechaFinal=dtfechaD.strftime("%Y-%m-%d")
                            if(fechaFinal<fechatest):
                                if(oportunity<16):
                                    oportunity=oportunity+1
                                else:
                                    salir=1
                            if(salir==1):
                                break
                    except Exception as e:
                        pass
                    #comprbamos si tenemos mas paginas por visitar
                    if temp["more_available"] == False:
                        next_max_id = False
                        break
                    #comenzamos el proceso de nuevo
                    next_max_id = temp["next_max_id"]
                    g = API.getHashtagFeed(hashtag,next_max_id)
                    temp = API.LastJson
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)


listaComments=['I have a course of python and Instagram , check my profile','course of python + instagram , check muy profile','good photo,check my profile','check my profile','good photo','check my first photo of python , instagram course free','instagram course free, check my profile']
ListHashtag=['pycoders','pythonprogramming','programmer','programmerslife','programming','programminglife','opensource','learntocode']
commentsByHashtag(ListHashtag,'2019-05-26',user,pwd)
 
