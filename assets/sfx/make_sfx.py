import numpy as np, wave, sys, os
SR=48000
out=sys.argv[1]; os.makedirs(out,exist_ok=True)
rng=np.random.default_rng(7)
def env_ad(n,att,dec):
    t=np.arange(n)/SR
    a=np.clip(t/att,0,1) if att>0 else np.ones(n)
    return a*np.exp(-np.maximum(t-att,0)/dec)
def lp(x,fc):
    # one-pole lowpass
    a=np.exp(-2*np.pi*fc/SR); y=np.zeros_like(x); s=0.0
    for i,v in enumerate(x): s=(1-a)*v+a*s; y[i]=s
    return y
def save(name,x,peak_db=-6.0):
    x=x-np.mean(x)
    fade=int(0.004*SR); x[:fade]*=np.linspace(0,1,fade); x[-fade:]*=np.linspace(1,0,fade)
    x=x/np.max(np.abs(x))*10**(peak_db/20)
    st=np.stack([x,x],1)
    with wave.open(os.path.join(out,name+'.wav'),'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st*32767).astype('<i2').tobytes())
    print(name, '%.2fs'%(len(x)/SR))
def tone(f,dur,att,dec,harm=()):
    n=int(dur*SR); t=np.arange(n)/SR
    x=np.sin(2*np.pi*f*t)
    for k,g in harm: x+=g*np.sin(2*np.pi*f*k*t)
    return x*env_ad(n,att,dec)
# 1 tick: soft high UI tap
x=tone(2100,0.09,0.0015,0.018,((2,0.25),))+0.15*lp(rng.standard_normal(int(0.09*SR)),5000)*env_ad(int(0.09*SR),0.0005,0.004)
save('tick',lp(x,7000),-9)
# 2 tap: warmer, for cards appearing (slight pitch drop)
n=int(0.22*SR); t=np.arange(n)/SR; f=620-120*(1-np.exp(-t/0.03))
x=np.sin(2*np.pi*np.cumsum(f)/SR)*env_ad(n,0.002,0.05)+0.3*np.sin(2*np.pi*2*np.cumsum(f)/SR)*env_ad(n,0.002,0.02)
save('tap',lp(x,4000),-8)
# 3 air: soft swish (bandpassed noise sweep)
def air(dur,peak,f0,f1,level=-10):
    n=int(dur*SR); t=np.arange(n)/SR
    noise=rng.standard_normal(n)
    # sweep by mixing two lowpasses (crude bandpass)
    fc=f0+(f1-f0)*np.clip(t/dur,0,1)
    y=np.zeros(n); s1=s2=0.0
    for i in range(n):
        a=np.exp(-2*np.pi*fc[i]/SR); s1=(1-a)*noise[i]+a*s1
        b=np.exp(-2*np.pi*(fc[i]*0.35)/SR); s2=(1-b)*noise[i]+b*s2
        y[i]=s1-s2
    e=np.where(t<peak,(t/peak)**2,np.exp(-(t-peak)/((dur-peak)/3.5)))
    return y*e
save('air',air(0.42,0.16,700,2600),-11)
save('air-long',air(1.1,0.82,300,2200),-9)
# 4 bloom: soft low emphasis for key findings
n=int(0.9*SR); t=np.arange(n)/SR
x=(np.sin(2*np.pi*196*t)+0.5*np.sin(2*np.pi*293.7*t)+0.25*np.sin(2*np.pi*392*t))*env_ad(n,0.035,0.28)
save('bloom',lp(x,2500),-7)
# 5 chime: gentle two-note bell for the final
def bell(f,dur):
    n=int(dur*SR); t=np.arange(n)/SR
    return (np.sin(2*np.pi*f*t)+0.35*np.sin(2*np.pi*f*2.76*t)*np.exp(-t/0.15))*env_ad(n,0.004,0.55)
a=bell(1046.5,1.6); b=bell(1568,1.6); d=int(0.11*SR)
x=np.zeros(len(a)+d); x[:len(a)]+=a; x[d:]+=0.8*b
save('chime-soft',lp(x,6000),-10)
# 6 drop ticks with slight pitch variation (marbles on the ruler)
for i in range(3):
    f=1500+i*180
    x=tone(f,0.08,0.001,0.014,((2.4,0.2),))
    save(f'drop-{i+1}',lp(x,6000),-10)
# 7 key: very soft key tick for typing
x=0.6*lp(rng.standard_normal(int(0.05*SR)),3500)*env_ad(int(0.05*SR),0.0005,0.006)+tone(1200,0.05,0.0005,0.008)*0.4
save('key',x,-14)
