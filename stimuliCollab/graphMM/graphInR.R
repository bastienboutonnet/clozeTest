library(reshape2)
library(ggplot2)

#Dat Loading
dat=read.csv('graph.csv',header=T)
# Rename columns for pretty labels
colnames(dat)=c("TextID","Type I Verb-initial",	"Type II Periphrastic",	"Type III Adj y VS",	"Type IV OaVS",	"Type IV SaVO",	"Type IV VN a DO")
#Convert To Long Format
df=melt(dat,id="TextID",variable.name="WordOrderType", value.name="Percentage")
#df=droplevels(subset(df, !(WordOrderType %in% c("Type.V.Focus", "Type.VIII.Sef"))))
#df$WordOrderType=levels(df$WordOrderType) <- c("one","two","three")
df$TextID=reorder(df$TextID, new.order=c("Laws",	"Culhwch",	"Pwyll",	"Branwen",	"Manawydan",	"Math",	"Peredur",	"Owein",	"Gereint",	"Rhonabwy",	"Macsen",	"Llud WB",	"Dewi","B1588"))
##Plot Style
PimpMyPlot <- theme(text=element_text(size=13,family="Helvetica"))+
  theme(axis.line=element_line(colour='black'))+
  theme(axis.text=element_text(colour="black"))+
  theme(panel.grid.major.y=element_line(linetype='dotted',colour='black',size=0.3))+
  theme(panel.grid.minor.y=element_blank())+
  theme(panel.grid.major.x=element_blank())+
  theme(axis.ticks=element_line(colour='black'))+
  theme(panel.background=element_rect(fill='transparent',colour="NA"))+
  theme(plot.background=element_rect(fill='transparent',colour="NA"))+
  #theme(axis.title=element_text(size=10,face="bold"))+
  theme(axis.title=element_blank())+
  theme(legend.key=element_blank())+
  theme(axis.text.x = element_text(angle = 45, hjust = 1))+
  
  
#Draw Plot
line=ggplot(df, aes(x=TextID,y=Percentage,group=WordOrderType))
line+geom_line(stat='identity',aes(colour=WordOrderType),size=.8)+
  geom_point(aes(colour=WordOrderType),size=2.5)+
  scale_y_continuous(breaks=seq(0,70,10),labels=c("0%","10%","20%","30%",'40%','50%','60%','70%'))+
  #scale_colour_discrete(name="Word-Order Type")+
  scale_color_manual(name="Word-Order Type",values =c('#da0017','#46a1f6','#40a439','#853492','#96431f','#ffd907'))+
  PimpMyPlot
#Save Plot
ggsave('plotnew.pdf',width=8, height=5)
