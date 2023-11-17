#Written by Nathan A-M =^)
#Buffer-based implementation using 
#A Buffer-based approach as a reference 

Bmin=10
Bmax=30
Blow=20
alpha1=0.33
alpha2=0.3
alpha3=0.4
alpha4=0.5
alpha5=0.65
runningFastStart=True




def student_entrypoint(previous_bitrate,previous_list,previous_throuput,av_bitrates,chunk_arg):
    #student can do whatever they want from here going forward
    global runningFastStart
    #print("algo start")
    #print(runningFastStart)
    Bdelay=0
    next_bitrate=previous_bitrate
    increasing=True
    if len(previous_list)==0:
        next_bitrate=min(av_bitrates,key=av_bitrates.get)
        return Bdelay,next_bitrate
    bitrate_set=list(av_bitrates.keys())
    bitrate_set.sort(key=lambda x: eval(x))
    for i in range(len(previous_list)-1):
        if previous_list[i][0]<previous_list[i+1][0]:
            increasing=False
            break
    average_bitrate=Average_bit_rate_calculation(previous_list)
    if runningFastStart and (previous_bitrate!=max(av_bitrates,key=av_bitrates.get)) and increasing and (previous_list[0][1]<alpha1*average_bitrate):
                    next_chunk_size= av_bitrates[bitrate_set[bitrate_set.index(previous_bitrate)+1]]
                    if previous_bitrate!=max(av_bitrates,key=av_bitrates.get):
                        next_bitrate=bitrate_set[bitrate_set.index(previous_bitrate)+1]
                    if previous_list[0][0]<Bmin:
                        if next_chunk_size<=alpha2*average_bitrate:
                            #print("1")
                            next_bitrate=bitrate_set[bitrate_set.index(previous_bitrate)+1]
                    elif previous_list[0][0]<Blow:
                        if next_chunk_size<=alpha3*average_bitrate:
                            #print("2")               
                            next_bitrate=bitrate_set[bitrate_set.index(previous_bitrate)+1]
                    else:
                        if next_chunk_size<=alpha4*average_bitrate: 
                            #print("3")              
                            next_bitrate=bitrate_set[bitrate_set.index(previous_bitrate)+1]
                        if previous_list[0][0]>Bmax:
                            #print("4")
                            Bdelay=Bmax-chunk_arg["time"]
    else:
        #print("staring stage end")
        runningFastStart=False
        if previous_list[0][0]<Bmin:
            #print("5")
            #print(previous_list[0][0])
            next_bitrate=min(av_bitrates,key=av_bitrates.get)
            #print(next_bitrate)
        elif previous_list[0][0]<Blow:
            #print(previous_list[0][0])             
            if (previous_bitrate!=min(av_bitrates,key=av_bitrates.get))and (previous_list[0][1]>=previous_throuput):
                #print("6")
                next_bitrate=bitrate_set[bitrate_set.index(previous_bitrate)-1]
            #else:
                #print("7")
        elif previous_list[0][0]<Bmax:
            #print(previous_list[0][0])
            if (previous_bitrate==max(av_bitrates,key=av_bitrates.get)):
                #print("8")                
                Bdelay=max(previous_list[0][0]-chunk_arg["time"],(Bmin+Bmax)/2)
            elif (av_bitrates[bitrate_set[bitrate_set.index(previous_bitrate)+1]]>=alpha5*average_bitrate):
                   # print("9")                              
                    Bdelay=max(previous_list[0][0]-chunk_arg["time"],(Bmin+Bmax)/2)
            #else:
               # print("10")                                    
        else:
            #print(previous_list[0][0])
            if (previous_bitrate==max(av_bitrates,key=av_bitrates.get)):
                #print("11")               
                Bdelay=max(previous_list[0][0]-chunk_arg["time"],(Bmin+Bmax)/2)
            elif (av_bitrates[bitrate_set[bitrate_set.index(previous_bitrate)+1]]>=alpha5*average_bitrate):
                   # print("12")               
                    Bdelay=max(previous_list[0][0]-chunk_arg["time"],(Bmin+Bmax)/2)
            else:
                   # print("13")               
                    next_bitrate=bitrate_set[bitrate_set.index(previous_bitrate)+1]
    return Bdelay,next_bitrate
      
          
def Average_bit_rate_calculation(previous_list):
    if len(previous_list)==0:
        return 0
    else:
        download_time=0
        total_size=0
        for i in range(len(previous_list)):
            download_time+=(previous_list[i][3]-previous_list[i][2])
            total_size+=previous_list[i][1]*8
        return (total_size/download_time)



