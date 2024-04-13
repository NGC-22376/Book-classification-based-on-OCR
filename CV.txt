#include <REG52.H>
#include <intrins.h>


sbit PWM = P3^7;
sfr ISP_CONTR  = 0xE7;
unsigned char count=0;
unsigned char timer1=2;
unsigned char time_all = 40;
unsigned char loop = 0;



void Timer0_Init(void)		//500us
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

void Delay500ms()		//@12.000MHz
{
	unsigned char i, j, k;

	_nop_();
	i = 4;
	j = 205;
	k = 187;
	do
	{
		do
		{
			while (--k);
		} while (--j);
	} while (--i);
}


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
	if (loop == 200){
		loop = 0;
    		ISP_CONTR = 0x60; 
  }
}


void main(){
	Timer0_Init();
	while(1){
	}
}