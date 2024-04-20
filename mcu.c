#include <REG52.H>
#include <intrins.h>

//����PWM������ź͸�λ�Ĵ���
sbit PWM = P2^7;
sfr ISP_CONTR  = 0xE7;
//�жϼ�����
unsigned char count=0;
//PWM�ź�һ�������ڸߵ�ƽʱ�����ʱ�䣬��0.5ms
unsigned char timer1=3;
unsigned char time_all = 40;
//��λ������
unsigned char loop = 0;


//�жϳ�ʼ����ÿ0.5ms�ж�һ��
void Timer0_Init(void)	
{
	TMOD &= 0xF0;		
	TMOD |= 0x01;		
	TL0 = 0x0C;
	TH0 = 0xFE;				
	TF0 = 0;				
	TR0 = 1;				
	
	ET0 = 1;      
	EA=1;
}

//�ж�ʱ��ִ������
void Timer0_Routine() interrupt 1{
	TL0 = 0x0C;
	TH0 = 0xFE;

	
	if (count <= timer1){
		PWM = 1;
	} else{
		PWM = 0;
	}
	count += 1;
	
	if (count == time_all){
		count = 0;
		loop += 1;
	}
	if (loop == 100){
		loop = 0;
    ISP_CONTR = 0x60; 
  }
}


void main(){
	Timer0_Init();
	while(1){
	}
}