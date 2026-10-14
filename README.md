# Reconocimiento de instrumentos musicales mediante análisis espectral

Proyecto de Teoría General de Señales.

La idea es que el programa reconozca qué instrumento suena en una grabación. Aunque dos instrumentos toquen la misma nota, el timbre cambia: se reparten distinto la energía entre los armónicos y el sonido ataca y se apaga de otra forma. Eso es lo que usamos para diferenciarlos.

## Los audios

Trabajamos con ocho instrumentos: clarinete, fagot, flauta, guitarra, piano, saxofón alto, trompeta y violín. Hay un audio .wav de cada uno en la carpeta data, tomados de bases de datos públicas de instrumentos y de grabaciones propias. Se usa .wav porque no comprime y no daña la información de frecuencias, a diferencia del mp3.

Antes de analizarlos, todos se pasan a mono y a una misma frecuencia de muestreo de 22050 Hz, y se usa el primer segundo de cada uno. Cada señal se normaliza para poder comparar instrumentos sin que influya qué tan fuerte se grabó.

## Qué se hace con la señal

Primero se mira cada audio en el tiempo y se revisa el efecto de la frecuencia de muestreo. Si se muestrea muy bajo, los armónicos altos se deforman (aliasing), así que se muestrea con margen sobre lo que pide Nyquist.

Después se pasa a frecuencia con la FFT, que muestra la frecuencia fundamental y los armónicos de cada instrumento, y con el espectrograma, que muestra cómo cambian en el tiempo.

Para el ruido se le agrega ruido a una grabación, como si estuviera mal grabada, y se limpia con un filtro pasa-bajos. Se compara la relación señal-ruido antes y después para ver cuánto mejora la señal.

## Cómo se reconoce el instrumento

Cada audio se parte en trozos cortos y de cada uno se sacan pocas características: el brillo del sonido (centroide espectral) y la altura del segundo, tercer y cuarto armónico. Con eso se entrena un clasificador KNN y se mide con precisión, recall y matriz de confusión. Para un audio nuevo se clasifica cada trozo y gana el instrumento que más veces salga.

Como solo hay una grabación por instrumento, la exactitud hay que tomarla con cuidado, por eso también se prueba con audios que no están en data.
