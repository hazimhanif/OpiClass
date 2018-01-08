func_clean_NA<-function(obs){
  
  if(as.character(obs$revAuthor)=="NA"){
    obs$revAuthor<-""
  }
  
  if(as.character(obs$revText)=="NA"){
    obs$revText<-""
  }
  obs
}

func_rev_pos_ascend<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  temp<-temp[order(temp$revDate,decreasing = FALSE),]
  which(temp[temp$appId==obs$appId,]$id==obs$id)
}

func_rev_pos_descend<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  temp<-temp[order(temp$revDate,decreasing = TRUE),]
  which(temp[temp$appId==obs$appId,]$id==obs$id)
}

func_first_rev<-function(obs){
  if(obs$revAuthor==""){
    return(1)
  }
  temp<-dataset[which(dataset$appId==obs$appId & dataset$revAuthor==obs$revAuthor),]
  temp<-temp[order(temp$revDate,decreasing = FALSE),]
  if(which(temp$id==obs$id)==1)
  {1}else{0}
}

func_only_rev<-function(obs){
  temp<-dataset[which(dataset$appId==obs$appId & dataset$revAuthor==obs$revAuthor),]
  if(nrow(temp)==1)
  {1}else{0}
}

func_avg_cosine_similarity_title<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  tempList<-c()
  for(x in seq(1,nrow(temp))){
    tempList<-c(tempList,stringdist(obs$revTitle,dataset[x,"revTitle"], method ="cosine"))
  }
  mean(tempList)
}

func_avg_cosine_similarity_text<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  tempList<-c()
  for(x in seq(1,nrow(temp))){
    tempList<-c(tempList,stringdist(obs$revText,dataset[x,"revText"], method ="cosine"))
  }
  tempList <- tempList[is.finite(tempList)]
  mean(tempList)
}

func_avg_levenshtein_dist_title<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  tempList<-c()
  for(x in seq(1,nrow(temp))){
    tempList<-c(tempList,stringdist(obs$revTitle,dataset[x,"revTitle"], method ="lv"))
  }
  mean(tempList)
}

func_avg_levenshtein_dist_text<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  tempList<-c()
  for(x in seq(1,nrow(temp))){
    tempList<-c(tempList,stringdist(obs$revText,dataset[x,"revText"], method ="lv"))
  }
  mean(tempList)
}

func_brand_names_in_title<-function(obs){
  if(length(grep(tolower(gsub(obs$revTitle,pattern = "[[:punct:]]",replacement = "")),pattern = tolower(gsub(obs$appTitle,pattern = "[[:punct:]]",replacement = ""))))==1){
    1
  }else{
    0
  }
}

func_brand_names_in_text<-function(obs){
  if(length(grep(tolower(gsub(obs$revText,pattern = "[[:punct:]]",replacement = "")),pattern = tolower(gsub(obs$appTitle,pattern = "[[:punct:]]",replacement = ""))))==1){
    1
  }else{
    0
  }
}

func_bad_rev_before<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  temp<-temp[order(temp$revDate,decreasing = FALSE),]
  x<-which(temp[temp$appId==obs$appId,]$id==obs$id)
  if(x==1){return(0)}
  if(temp[x-1,"label_sentiment"]=="negative"){1}else{0}
}

func_bad_rev_after<-function(obs){
  temp<-dataset[dataset$appId==obs$appId,]
  temp<-temp[order(temp$revDate,decreasing = FALSE),]
  x<-which(temp[temp$appId==obs$appId,]$id==obs$id)
  if(x==nrow(temp)){return(0)}
  if(temp[x+1,"label_sentiment"]=="negative"){1}else{0}
}

func_avg_words_freq_title<-function(obs){
  temp<-gsub(obs$revTitle,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp<-table(temp)
  mean(temp)
}

func_avg_words_freq_text<-function(obs){
  temp<-gsub(obs$revText,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp<-table(temp)
  mean(temp)
}

func_num_unique_words_title<-function(obs){
  temp<-gsub(obs$revTitle,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp<-table(temp)
  length(temp)
}

func_num_unique_words_text<-function(obs){
  temp<-gsub(obs$revText,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp<-table(temp)
  length(temp)
}

func_unique_words_to_words_title_ratio<-function(obs){
  temp<-gsub(obs$revTitle,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp1<-table(temp)
  length(temp1)/length(unlist(temp))
}

func_unique_words_to_words_text_ratio<-function(obs){
  temp<-gsub(obs$revText,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp1<-table(temp)
  length(temp1)/length(unlist(temp))
}

func_stdev_num_words_title_text<-function(obs){
  temp<-gsub(obs$revTitle,pattern = "[[:punct:]]",replacement = "")
  temp<-strsplit(temp," ")
  temp1<-gsub(obs$revText,pattern = "[[:punct:]]",replacement = "")
  temp1<-strsplit(temp1," ")
  sd(c(length(unlist(temp)),length(unlist(temp1))))
}



#### THIS IS THE NEW ADDITION

func_avg_num_letters_per_word<-function(obs){
  temp <- stri_replace_all(obs$revText, regex = "[^a-zA-Z0-9\\s]", replacement = "")
  stri_length(temp)/length(stri_split(temp,fixed = " ")[[1]])
}


func_stdev_revrating_avgrevratingapp<-function(obs,dataset){
  temp <- mean(dataset[dataset$appId==obs$appId,"revRating"])
  sd(c(obs$revRating,temp))
}

### Ini utk english
# func_polarity_text<-function(obs){
#   temp <- stri_replace_all(obs$revText, regex = "[^a-zA-Z0-9\\s]", replacement = "")
#   lev<-as.double(calculate_score(temp)[[1]])
#   if(lev<0){
#     lev<-0
#   }else if(lev==0){
#     lev<-1
#   }else if(lev==99){
#     lev<-3
#   }else if(lev>0){
#     lev<-2
#   }else{
#     lev <- lev
#   }
#  lev
# }

### jgn guna features ni
# func_rev_inconsistent<-function(obs){
#   
#   if(polarity_text==0 & obs$revRating<3){
#     rev_inconsistent <- 0
#     
#   }else if(polarity_text==0 & obs$revRating>3){
#     rev_inconsistent <- 1
#     
#   }else if(polarity_text==0 & obs$revRating==3){
#     rev_inconsistent <- 1
#     
#   }else if(polarity_text==2 & obs$revRating<3){
#     rev_inconsistent <- 1
#     
#   }else if(polarity_text==2 & obs$revRating>3){
#     rev_inconsistent <- 0
#     
#   }else if(polarity_text==2 & obs$revRating==3){
#     rev_inconsistent <- 1
#     
#   }else if(polarity_text==1 & obs$revRating<3){
#     rev_inconsistent <- 1
#     
#   }else if(polarity_text==1 & obs$revRating>3){
#     rev_inconsistent <- 1
#     
#   }else if(polarity_text==1 & obs$revRating==3){
#     rev_inconsistent <- 0
#     
#   }else if(polarity_text==3){
#     rev_inconsistent <- 1
#     
#   }else{
#     rev_inconsistent <- 0
#   }
#   
#   rev_inconsistent
#   
# }

### Ini utk melayu
func_polarity_text<-function(obs){
  sum_neg <- 0
  sum_pos <- 0
  for(i in 1:length(positive_words)){
    sum_pos <- sum_pos + length(grep(obs$revText,pattern = positive_words[i]))
  }

  for(i in 1:length(negative_words)){
    sum_neg <- sum_neg + length(grep(obs$revText,pattern = negative_words[i]))
  }


  if(sum_neg>sum_pos){
    lev<-0
  }else if(sum_pos>sum_neg){
    lev<-2
  }else{
    lev<-1
  }
  lev
}

func_automated_readability_index_text<-function(obs){
  
  ari <- as.double(4.71*(stri_length(obs$revText)/stri_count_words(obs$revText))+0.5*(stri_count_words(obs$revText)/length(stri_split(obs$revText,fixed = ".")[[1]]))-21.43)
  ari
}


positive_words<-c("ok","baik","suka","bgus","bagus","bagos","tepat","mudah","thank","boleh",
                 "best","seronok","senang","hebat","good","elok","suke","puas","baek","layan","boek","gempak",
                 "syok","lucu","sedap","bleh","sdp","menyeronokkon","bagus",
                 "comel","menyenangkan","bantu","syiok","blh la","menyukainya","boleh la",
                 "maju","macho","hensem","bergaya","cool","pandai","pndi","sempoi","bereh","merdu","subhanallah","alhamdulillah",
                 "syukur","amin","wajib","wajip","allah","memuaskan","berkesan","baguh","bgs","okey","manfaat","terima kasih",
                 "kekuatan","jelas","cepat","laju","boleh tahan","ok sangat","lucu","lwk","lawak","kelakar","sesuai","ssuai","menyukai",
                 "rancak","nice","besnya","bes gila","bes gile","shok",'👍','😜','😙','😄','😊','😉')

negative_words<-c("babi","bodoh","anjing","lancau","kote","pantat","setan","bahalol","bangang","sial","buto",
                  "pundek","bosan","busuk","mati","kecewa","bodo","bangla","geram","natang","mapuh","puki","kontol",
                  "pepek","pantek","setan","lembab","fuck","cipap","burit","haram","susah","adui","adoi","menyusah","menyusahkan",
                  "jilake","wtf","fck","cb","badigol","bladigol","ssh","jadah","kimak","siak","rugi","teruk","terok",
                  "lag","tak best","tak best","tk bes","tk best","penipu","tipu","rosak","syaitan","banggang","benci","lahanat","cibai","lama","lame","taik",
                  "vabi","fvck","fcuk","babun","bangsat","bongek","kiwak","gampang","tak","tidak","konek","sex","jubo","jubu",
                  "jubur","jubor","buntut","bontot","habis","abis","barai","mampus","mampos","xleh","penat","bahabi","punay",
                  "puney","bana","fucking","benci","lambat","lembap","butuh","telo","ngarot","tk")
