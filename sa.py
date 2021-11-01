import numpy as nb
import pandas as bd
import numpy.linalg as lng
import matplotlib.pyplot as ltb
#veri okuma
veri = bd.read_excel("mobilephoneprice.xlsx")
#satır seçme
veri_seti=veri.loc[1:2001:3]
#seçilen satırlardan bir array oluşturma
veri_seti_array=nb.array(veri_seti,dtype=int)
#array in üzerinde gerekli işlemler yapıldıktan sonra oluşturulacak yeni veri seti
veri_seti_son=nb.zeros((667,20),dtype=int)
#1. bölüm sayıssal tipteki kolonların alınarak merkezden iki standart sapma uzaklıktaki verilerin ortalama ile değiştirilmesi
#veri setinde 20 sayısal kolon olduğu için 20 kolon for döngüsünde gezdirildi
silinen_list=[]
for x in range(20):
    #numpy.std methodu ile x kolonunun standart sapması hesaplandı.
    standart = nb.std(veri_seti_array[:, x])
    #ortalama numpy.average methodu ile hesaplanıp bir değişkene atıldı
    ort = nb.average(veri_seti_array[:, x])
    #kolon tek boyutlu bir diziye aktarıldı
    veri_seti_array_x=nb.array(veri_seti_array[:,x],dtype=int)
    #kolon bir for döngüsüne gönderildi
    for y in range(veri_seti_array_x.size):
        #her bir veri için ortalamadan uzaklığı hesaplandı ve standart sapmanın 2 katı alınarak kontrol edildi
        if(nb.absolute(ort-(veri_seti_array_x[y]))>2*standart):
            #silinecek veriler burada konsola yazdırılarak rapor edildi
            silinen_list.append(veri_seti_array_x[y])
            #eğer ortalamadan uzaklığı 2 * standart sapmadan büyükse, değer o kolonun ortalaması ile değiştirildi
            nb.put(veri_seti_array_x,y,ort)
            #print(veri_seti_array_x[y]) bu kısımda verileri silinip silinmediğini kontrol ettim
        #else:
            #print(veri_seti_array_x[y],"veri silinmedi ",x,y)
    #yukarıda oluşturulan yeni veri dizisi son olacak toplam diziye kolon kolon aktarıldı
    veri_seti_son[:,x]=veri_seti_array_x
print(silinen_list)
print(len(silinen_list))

#veri yazdırma fonksiyonu
def yazdir_veri(array):
    for x in range(20):
        for y in array[:,x]:
            print(y)

#2. bölüm histogram yazdırma
name_list=nb.zeros(20)
name_list_array=list(name_list)
name_list_imp=["bluetooth","dualsim","4g","touch_screen","wifi","price_range"]
count=0

for x in range(20):
    if(x==1 or x==3 or x==5  or x==17 or x==18 or x==19):
        name_list_array.insert(x,name_list_imp[count])
        count=count+1

for z in range(20):
    if (z == 1 or z == 3 or z == 5 or z == 17 or z == 18 or z == 19):
        #bu kısımda pythonun matplotlib isimli kütüphanesi import edildi ve histogram çizdirildi.
        #kategorik verilerde herhangi bir uçuk veri bulunmadığı için herhangi bir veri silinmedi
        ltb.hist(veri_seti_array[:,z],bins=50)
        ltb.title(name_list_array[z])
        ltb.show()
#dizinin içinde istenen elemandan bulunup bulunmadığını kontrol eden method
def contains(array,obj):
    for x in array:
        if(x==obj):
            return True
    return False
#entropi bulma ve sıralama methodu parametre olarak 2 boyutlu bir dizi ve kolon numarası alınıyor
def find_entropy(array,ind):
    list1=[]
    ent=0;
#iki boyutlu dizinin "ind" kolonundaki veriler for döngüsüyle gezdiriliyor
    for x in array[:,ind]:
        #bu kısımda kategorik biçimde bulunan kolonların kategorileri bir diziye aktarılıyor
        if(not(contains(list1,x))):
            list1.append(x)
    list2 = [len(list1)]
    #burada dizinin içinde her kategoriden kaç eleman bulunduğu list2'ye aktarılıyor
    for x in array[:,ind]:
        for y in range(len(list1)):
            if(x==list1[y]):
                list2.insert(list2[y]+1,y)
    for y in list1:
        #burada count metodunu kullanabilmek için numpy array liste haline getiriliyor
        templist=array[:,ind].tolist()
        #entropi hesabı
        ent+=(templist.count(y)/len(templist)*nb.log((templist.count(y)/len(templist))))
    return -ent
#sayısal veri kolonlarının entropi sıralaması
ent_sira=[]
for x in range(20):
    if x == 1 or x == 3 or x == 5 or x == 17 or x == 18 or x == 19:
        ent_temp=find_entropy(veri_seti_array,x)
        ent_sira.append(ent_temp)
ent_sira.sort()
print("ent_sira",ent_sira)
#fiyat aralığı kolonunun entropisi
fiyat_ent=find_entropy(veri_seti_array,19)
print("fiyat aralığı entropisi: ",fiyat_ent)
#burada information gain hesabı yaptırılıyor
#bluetooth dual sim ve 4g özelliklerin fiyat aralığına uyguladığı değişim görülüyor
# burası sıralama için oluşturulan dizi
gain_sira = []
for x in range(20):
    if x == 1 or x == 3 or x == 5 or x == 17 or x == 18:
        #burada özelliklere sahip olan telefonların indisleri alınıyor
        blue_list=veri_seti_array[:,x].nonzero()
        #burada liste uzlunluğunu öğrenmek için listeye çevrilip len methodu kullanılıyor
        len_list=list(blue_list)
        print("1list: ",len(len_list[0]),"0list: ",len(veri_seti_array[:,x])-len(len_list[0]))
        #burada a_ent ve b_ent özelliğe sahip olan ve olmayan telefonların ayrı ayrı entropilerini ifade ediyor
        a_ent=-((len(len_list[0])/len(veri_seti_array[:,x]))*nb.log(len(len_list[0])/len(veri_seti_array[:,x])))
        b_ent=-(((len(veri_seti_array[:,x])-len(len_list[0]))/len(veri_seti_array[:,x]))*nb.log((len(veri_seti_array[:,x])-len(len_list[0]))/len(veri_seti_array[:,x])))
        print("a ",a_ent,"b ", b_ent)
        #burası information gain hesabı
        #değeri 1 olanların entropilerinin sayı oranlarıyla çarpımı
        gain_a=a_ent*(len(len_list[0])/len(veri_seti_array[:,x]))
        #değeri 0 olanların entropilerinin sayı oranlarıyla çarpımı
        gain_b=b_ent*((len(veri_seti_array[:,x])-len(len_list[0]))/len(veri_seti_array[:,x]))
        #fiyat aralığı kolonunun entropisinden toplam entropileri çıkarılarak gainimizi öğrenmiş oluyoruz
        gain=fiyat_ent-(gain_a+gain_b)
        gain_sira.append(gain)
        print("gain= ",gain)
#gainlerin küçükten büyüğe sıralanışı
gain_sira.sort()
print("gain_sıra",gain_sira)


