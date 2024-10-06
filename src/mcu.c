#include <REG52.H>
#include <intrins.h>

//设置PWM输出引脚和复位寄存器
sbit PWM = P2^7;
sfr ISP_CONTR  = 0xE7;
//中断计数器
unsigned char count=0;
//PWM信号一个周期内高电平时间和总时间，乘0.5ms
unsigned char timer1=3;
unsigned char time_all = 40;
//复位计数器
unsigned char loop = 0;


//中断初始化，每0.5ms中断一次
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

//中断时的执行内容
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