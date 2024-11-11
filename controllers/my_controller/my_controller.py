"""
Alunos:

    Carlos Massato Horibe Chinen (R.A: 22.221.010-6)
    Gabriel Nunes Missima        (R.A: 22.221.040-3)
    Vinicius Alves Pedro         (R.A: 22.221.036-1)
"""

from controller import Robot, Supervisor, LED

TIME_STEP = 32
MAX_SPEED = 6.28
WAIT_TIME = 64.0

def iniciar(meuRobo, supervisor):
    motorEsquerdo = meuRobo.getDevice("left wheel motor");
    motorDireito = meuRobo.getDevice("right wheel motor");
    
    motorEsquerdo.setPosition(float('inf'))
    motorDireito.setPosition(float('inf'))
    
    motorEsquerdo.setVelocity(0.0)
    motorDireito.setVelocity(0.0)
    
    caixa = supervisor.getFromDef("caixa_leve")
    
    sensor = []
    for i in range(8):
        sensor.append(meuRobo.getDevice(f"ps{i}"))
        sensor[i].enable(TIME_STEP)
    
    led = []
    for i in range(10):
        led.append(meuRobo.getDevice(f"led{i}"))
        led[i].set(0)
        
    TIMER = 0.0
    LOCK = False

    while meuRobo.step(TIME_STEP) != -1:
        TIMER += 1.0
        encontrou = False
        
        caixaPos = caixa.getPosition()
        
        if TIMER == WAIT_TIME:
            caixaInit = caixa.getPosition()
            LOCK = True
            print("Caixa não se move mais sozinha")
                
        if LOCK:
            if caixaInit != caixaPos:
                encontrou = True
        
        if encontrou:
            viradaEsquerda = 0.0
            viradaDireita = 0.0
            motorEsquerdo.setVelocity(0.0)
            motorDireito.setVelocity(0.0)
    
            for i in range(10):
                led[i].set(1)
    
            print('CAIXA ENCONTRADA')
            break

        viradaEsquerda = MAX_SPEED / 1.25
        viradaDireita = MAX_SPEED / 1.25
        
        sensorDireitoAtivo = False
        sensorEsquerdoAtivo = False
    
        for i in range(4):
            if sensor[i].getValue() > 100:
                sensorDireitoAtivo = True
                viradaEsquerda = 0.25 * MAX_SPEED
                viradaDireita = MAX_SPEED
                
                break
                
        for i in range(4, 8):
            if sensor[i].getValue() > 100:
                sensorEsquerdoAtivo = True
                viradaEsquerda = MAX_SPEED
                viradaDireita = 0.25 * MAX_SPEED
                break
                
        if sensorDireitoAtivo and sensorEsquerdoAtivo:
            viradaEsquerda = -MAX_SPEED
            viradaDireita = MAX_SPEED
    
        motorEsquerdo.setVelocity(viradaEsquerda)
        motorDireito.setVelocity(viradaDireita)

        pass

if __name__ == "__main__":
    meuRobo = Robot()
    supervisor = Supervisor() 
    iniciar(meuRobo, supervisor)
