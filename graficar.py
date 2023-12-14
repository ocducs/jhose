import shutil

def plotear(x,y,plt,imei):
    
    _x = [0,360,360,0,int(x)]
    _y = [355,355,0,0,int(y)]
    n=['AP1','AP2','AP3','AP4','Device']
    fig, ax = plt.subplots()
    ax.scatter(_x, _y)

    for i, txt in enumerate(n):
        ax.annotate(txt, (_x[i], _y[i]))
    from datetime import datetime
    plt.title(f"IMEI: {imei} Hora: {datetime.now()}")
    
    try:
        plt.savefig(f'Device_{imei}.png')
        
        #shutil.copyfile('grafica_original.png', 'grafica.png')
        
    except Exception as e:
        print(e)

    del plt