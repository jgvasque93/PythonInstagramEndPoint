from InstagramAPI import InstagramAPI
import time
from datetime import datetime
import sys
user = 'User'
pwd = 'password'

def likesByHashtag(ListHashtag,fechatest,user,pwd):
    #login en el Api de instagram
    API = InstagramAPI(user,pwd)
    print('login:',user,pwd)
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
                        n = randint(50,90)
                        time.sleep(3*n)
                        g = API.getHashtagFeed(hashtag,next_max_id)
                        temp = API.LastJson
                    #recorremos nyestro json respuesta
                    salir=0
                    for item in temp["items"]:
                        #obtenemos el id del post y se lo mandamos a la funcion like() del Api
                        rp=API.like(item['id'])
                        if(rp):
                            contadorLikes=contadorLikes+1
                        print('likes para hashtag:',hashtag,contadorLikes)
                        #esperamos 25 segundos para no excder el limite de likes de instagram de 100 por hora
                        time.sleep(25)
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
                            rp=API.like(item['id'])
                            if(rp):
                                contadorLikes=contadorLikes+1
                            print('likes para hashtag:',hashtag,contadorLikes)
                            time.sleep(25)
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



ListHashtag=['like4follow','followforfollowback','followme','follow_me']
likesByHashtag(ListHashtag,'2019-05-03',user,pwd)
