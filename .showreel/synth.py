# Banda sonora original del showreel (58 s, 48 kHz), sincronizada con los cortes de showreel.html.
import numpy as np, wave
SR=48000; D=58.0; N=int(SR*D)
rng=np.random.default_rng(7)
L=np.zeros(N); R=np.zeros(N)
def add(sig,t,gain=1.0,pan=0.0):
    i=int(t*SR); n=min(len(sig),N-i)
    if n<=0: return
    l=np.cos((pan+1)*np.pi/4); r=np.sin((pan+1)*np.pi/4)
    L[i:i+n]+=sig[:n]*gain*l*1.414; R[i:i+n]+=sig[:n]*gain*r*1.414
def env(n,a,d_rel):  # ataque lineal + caída exponencial
    t=np.arange(n)/SR; e=np.minimum(1,t/max(a,1e-4))*np.exp(-t/d_rel); return e
def lp(x,a):  # filtro paso bajo de un polo
    y=np.empty_like(x); s=0.0
    for i in range(len(x)): s+=a*(x[i]-s); y[i]=s
    return y
def lp_fast(x,cut):
    # paso bajo en frecuencia (sin bucle)
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X*=1/(1+(f/cut)**4); return np.fft.irfft(X,len(x))
def hp_fast(x,cut):
    X=np.fft.rfft(x); f=np.fft.rfftfreq(len(x),1/SR); X*=1/(1+(cut/np.maximum(f,1))**4); return np.fft.irfft(X,len(x))
midi=lambda m:440*2**((m-69)/12)

# --- instrumentos
def kick():
    n=int(.45*SR); t=np.arange(n)/SR
    f=45+110*np.exp(-t*28); ph=2*np.pi*np.cumsum(f)/SR
    return np.sin(ph)*np.exp(-t*7.5)*1.0 + np.sin(ph*2)*np.exp(-t*40)*.15
def hat(open_=False):
    n=int((.25 if open_ else .06)*SR); x=hp_fast(rng.standard_normal(n),7000)
    return x*env(n,.001,.08 if open_ else .018)
def clap():
    n=int(.3*SR); x=hp_fast(lp_fast(rng.standard_normal(n),5000),900)
    e=np.zeros(n)
    for d in (0,.011,.022): i=int(d*SR); e[i:]+=np.exp(-np.arange(n-i)/SR/.045)
    return x*e*.5
def pad(notes,dur):
    n=int(dur*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for m in notes:
        for det in (-0.08,0.0,0.08):
            f=midi(m)*2**(det/12); ph=rng.uniform(0,6.28)
            x+=(2*((f*t+ph/6.28)%1)-1)*.33          # sierra desafinada
    x=lp_fast(x,1400)
    a=np.minimum(1,t/1.2)*np.minimum(1,(dur-t)/1.0).clip(0,1)
    return x*a/len(notes)
def pluck(m,dur=.35):
    n=int(dur*SR); t=np.arange(n)/SR; f=midi(m)
    x=(2*((f*t)%1)-1)+.5*np.sin(2*np.pi*f*2*t)
    return lp_fast(x,2600)*env(n,.002,.11)
def bass(m,dur):
    n=int(dur*SR); t=np.arange(n)/SR; f=midi(m)
    x=np.sin(2*np.pi*f*t)+.25*np.sin(2*np.pi*2*f*t)
    return x*np.minimum(1,t/.01)*np.exp(-t/.5)*np.minimum(1,(dur-t)/.03).clip(0,1)
def whoosh(dur=.9,rev=False):
    n=int(dur*SR); t=np.arange(n)/SR; x=rng.standard_normal(n)
    # barrido: filtrado por bloques con corte creciente
    out=np.zeros(n); B=2048
    for i in range(0,n,B):
        k=i/n; cut=300+6000*(k**2)
        out[i:i+B]=lp_fast(x[i:i+B],cut)[:len(out[i:i+B])]
    e=np.sin(np.pi*np.minimum(1,t/dur))**2
    y=out*e; return y[::-1] if rev else y
def riser(dur):
    n=int(dur*SR); t=np.arange(n)/SR
    f=200*2**(t/dur*3); ph=2*np.pi*np.cumsum(f)/SR
    x=.35*np.sin(ph)+.6*whoosh(dur)
    return x*(t/dur)**2
def boom():
    n=int(3.0*SR); t=np.arange(n)/SR
    f=38+60*np.exp(-t*6); ph=2*np.pi*np.cumsum(f)/SR
    x=np.sin(ph)*np.exp(-t*1.6)+.4*lp_fast(rng.standard_normal(n),900)*np.exp(-t*3)
    return x
def click():
    n=int(.05*SR); t=np.arange(n)/SR
    return np.sin(2*np.pi*1800*t)*np.exp(-t*160)+.3*hp_fast(rng.standard_normal(n),4000)*np.exp(-t*300)
def chime(ms):
    n=int(1.6*SR); t=np.arange(n)/SR; x=np.zeros(n)
    for j,m in enumerate(ms):
        i=int(j*.06*SR); f=midi(m)
        x[i:]+=np.sin(2*np.pi*f*t[:n-i])*np.exp(-t[:n-i]*3)*.5+np.sin(2*np.pi*f*3*t[:n-i])*np.exp(-t[:n-i]*9)*.1
    return x
def tick():
    n=int(.03*SR); t=np.arange(n)/SR
    return np.sin(2*np.pi*3200*t)*np.exp(-t*250)

# --- arreglo
BEAT=.5; T0=11.0                      # 120 BPM, compás anclado al revelado del logo
# intro (0–11): dron grave, tic-tac, presupuestos que no cuadran
add(pad([45,52,57],11.2),0,.55)
add(bass(33,11.0)*np.linspace(.2,1,int(11*SR)),0,.25)
for k in range(22): add(tick(),0.5+k*.5,.10 if k%2 else .16,pan=(-.4 if k%2 else .4))
add(riser(2.2),8.8,.55)
add(boom(),T0,.9); add(whoosh(1.2,rev=True),T0-1.2,.3)
# groove (11–53.6)
PROG=[[57,60,64],[53,57,60],[48,55,60],[55,59,62]]   # Am F C G
ROOT=[33,29,36,31]
end=53.6
nbar=int((end-T0)/(4*BEAT))
for b in range(nbar):
    tb=T0+b*4*BEAT; ch=(b//1)%4
    add(pad(PROG[ch],4*BEAT+.6),tb,.42)
    for q in range(4):
        tq=tb+q*BEAT
        if b>=2 or q>=0: add(kick(),tq,.85 if b>=2 else .55)
        add(hat(),tq+BEAT/2,.16,pan=.3)
        if b>=2 and q in (1,3): add(clap(),tq,.35,pan=-.1)
        add(bass(ROOT[ch]+(12 if q==3 else 0),BEAT*.9),tq,.55)
    # arpegio en corcheas a partir del compás 2
    if b>=2:
        arp=PROG[ch]+[PROG[ch][1]+12]
        for e in range(8): add(pluck(arp[e%4]+12,.3),tb+e*BEAT/2,.12,pan=(-.5 if e%2 else .5))
# transiciones y UI
for tt in [5.1,15.0,20.3,25.12,29.94,34.76,39.58,44.1,49.0]: add(whoosh(.8),tt-.45,.28)
add(click(),27.1,.5); add(chime([76,81,84]),27.25,.18)                 # pago y desbloqueo
add(click(),37.35,.5); add(chime([72,76,79,84]),37.5,.22)              # adjudicación
for k in range(6): add(tick(),31.05+k*.36,.08)                         # tecleo de precios
# final (53.6–58)
add(riser(1.6),52.0,.35)
add(boom(),end,.8)
add(pad([57,61,64,69],4.4),end,.7)                                       # La mayor, resolución
add(chime([81,85,88,93]),end+.05,.2)
# reverb sencilla (convolución con cola de ruido)
ir_n=int(1.8*SR); ir=rng.standard_normal(ir_n)*np.exp(-np.arange(ir_n)/SR/.45); ir/=np.sqrt((ir**2).sum())
def conv(x):
    m=len(x)+ir_n; F=1<<(m-1).bit_length()
    return np.fft.irfft(np.fft.rfft(x,F)*np.fft.rfft(ir,F),F)[:len(x)]
L=L+.22*conv(L); R=R+.22*conv(R)
# fundidos y master
fade=np.ones(N); fi=int(.3*SR); fade[:fi]=np.linspace(0,1,fi); fo=int(2.2*SR); fade[-fo:]=np.linspace(1,0,fo)**1.5
L*=fade; R*=fade
peak=max(np.abs(L).max(),np.abs(R).max()); L/=peak; R/=peak
L=np.tanh(L*1.6)/np.tanh(1.6)*.89; R=np.tanh(R*1.6)/np.tanh(1.6)*.89
out=(np.stack([L,R],1)*32767).astype('<i2')
with wave.open('music.wav','wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print('ok',N/SR)
