args = commandArgs(trailingOnly=TRUE)

## Importing library
library(stringdist)
library(stringr)
library(stringi)
library(RSentiment)
library(jsonlite)
#library(car)
library(gbm)

## Set WD
setwd("/home/hazim/OpiClass")

## Source the functions file
source("r_scripts/yelp_func.R")

##Reading file
dataset <- fromJSON(txt=paste("data/filtered_reviews/",args[1],".json",sep = ""),flatten = TRUE)
dataset$id <- seq(1,nrow(dataset))

print("Converting date data to real date type.")
month_list<-list()
{
  month_list[["Januari"]]<-"01"
  month_list[["Februari"]]<-"02"
  month_list[["Mac"]]<-"03"
  month_list[["April"]]<-"04"
  month_list[["Mei"]]<-"05"
  month_list[["Jun"]]<-"06"
  month_list[["Julai"]]<-"07"
  month_list[["Ogos"]]<-"08"
  month_list[["September"]]<-"09"
  month_list[["Oktober"]]<-"10"
  month_list[["November"]]<-"11"
  month_list[["Disember"]]<-"12"
}


for(x in seq(1,nrow(dataset))){
  tempsplit<-strsplit(x=dataset[x,"revDate"],split =" ")
  dataset[x,"revDate"]<-paste(tempsplit[[1]][1],month_list[[tempsplit[[1]][2]]],tempsplit[[1]][3],sep = "-")
}
dataset$revDate<-as.Date(dataset$revDate,"%d-%m-%Y")

##List init
mylist<-list()

print("Features extraction...")

for(x in seq(1,nrow(dataset))){
  obs<-dataset[x,]
  
  obs<-func_clean_NA(obs)
  
  ##Features Extraction: Total 37
#  print(x)
  ##Continuos values features
  app_score<-as.double(obs$appScore)
  rev_body_len<-str_length(obs$revText)
  rev_pos_ascend<-func_rev_pos_ascend(obs)
  rev_pos_descend<-func_rev_pos_descend(obs)
  avg_cosine_similarity_text<-func_avg_cosine_similarity_text(obs)
  avg_levenshtein_dist_text<-func_avg_levenshtein_dist_text(obs)
  numeric_text_ratio<-length(as.numeric(unlist(strsplit(gsub("[^0-9]", "", unlist(obs$revText)), ""))))/str_length(obs$revText)
  #cap_words_ratio<-length(unlist(str_extract_all(obs$revText, '\\b[A-Z]+\\b')))/length(unlist(str_split(obs$revText,pattern = " ")))
  #num_cap_letters_ratio<-length(unlist(str_extract_all(obs$revText, '[A-Z]')))/length(unlist(str_extract_all(obs$revText, '[A-Za-z]')))
  rev_rating<-as.numeric(obs$revRating)
  stdev_revApp_rating<-sd(c(as.double(obs$revRating),as.double(obs$appScore)))
  avg_words_freq_text<-func_avg_words_freq_text(obs)
  num_unique_words_text<-func_num_unique_words_text(obs)
  unique_words_to_words_text_ratio<-func_unique_words_to_words_text_ratio(obs)
  avg_num_letters_per_word<-func_avg_num_letters_per_word(obs)
  stdev_revrating_avgrevratingapp<-func_stdev_revrating_avgrevratingapp(obs,dataset)
  automated_readability_index_text<-func_automated_readability_index_text(obs)
  
  avg_cosine_similarity_title<-func_avg_cosine_similarity_title(obs)
  avg_levenshtein_dist_title<-func_avg_levenshtein_dist_title(obs)
  avg_words_freq_title<-func_avg_words_freq_title(obs)
  num_unique_words_title<-func_num_unique_words_title(obs)
  unique_words_to_words_title_ratio<-func_unique_words_to_words_title_ratio(obs)
  stdev_num_words_title_text<-func_stdev_num_words_title_text(obs)
  
  
  ##Categorical features
  brand_names_in_title<-func_brand_names_in_title(obs)
  
  first_rev<-func_first_rev(obs)
  only_rev<-func_only_rev(obs)
  brand_names_in_text<-func_brand_names_in_text(obs)
  polarity_text<-func_polarity_text(obs)
  #rev_inconsistent<-func_rev_inconsistent(obs)
  ##Label
  #class<-obs$label_authenticity
  
  
  #mylist[[x]]<-c(app_score,rev_body_len,rev_pos_ascend,rev_pos_descend,avg_cosine_similarity_text,avg_levenshtein_dist_text,numeric_text_ratio,cap_words_ratio,num_cap_letters_ratio,rev_rating,stdev_revApp_rating,avg_words_freq_text,num_unique_words_text,unique_words_to_words_text_ratio,avg_num_letters_per_word,stdev_revrating_avgrevratingapp,automated_readability_index_text,avg_cosine_similarity_title,avg_levenshtein_dist_title,brand_names_in_title,avg_words_freq_title,num_unique_words_title,unique_words_to_words_title_ratio,stdev_num_words_title_text,first_rev,only_rev,brand_names_in_text,polarity_text,rev_inconsistent,class)
   mylist[[x]]<-c(app_score,rev_body_len,rev_pos_ascend,rev_pos_descend,avg_cosine_similarity_text,avg_levenshtein_dist_text,numeric_text_ratio,rev_rating,stdev_revApp_rating,avg_words_freq_text,num_unique_words_text,unique_words_to_words_text_ratio,avg_num_letters_per_word,stdev_revrating_avgrevratingapp,automated_readability_index_text,avg_cosine_similarity_title,avg_levenshtein_dist_title,brand_names_in_title,avg_words_freq_title,num_unique_words_title,unique_words_to_words_title_ratio,stdev_num_words_title_text,first_rev,only_rev,brand_names_in_text,polarity_text)
  
  
  #    if(x==100000){
  #     break
  #    }
  gc()
}

df_dataset<-data.frame(t(sapply(mylist,c)))
#names(df_dataset)<-c("app_score","rev_body_len","rev_pos_ascend","rev_pos_descend","avg_cosine_similarity_text","avg_levenshtein_dist_text","numeric_text_ratio","rev_rating","stdev_revApp_rating","avg_words_freq_text","num_unique_words_text","unique_words_to_words_text_ratio","avg_num_letters_per_word","stdev_revrating_avgrevratingapp","automated_readability_index_text","avg_cosine_similarity_title","avg_levenshtein_dist_title","brand_names_in_title","avg_words_freq_title","num_unique_words_title","unique_words_to_words_title_ratio","stdev_num_words_title_text","first_rev","only_rev","brand_names_in_text","polarity_text","rev_inconsistent","class")
names(df_dataset)<-c("app_score","rev_body_len","rev_pos_ascend","rev_pos_descend","avg_cosine_similarity_text","avg_levenshtein_dist_text","numeric_text_ratio","rev_rating","stdev_revApp_rating","avg_words_freq_text","num_unique_words_text","unique_words_to_words_text_ratio","avg_num_letters_per_word","stdev_revrating_avgrevratingapp","automated_readability_index_text","avg_cosine_similarity_title","avg_levenshtein_dist_title","brand_names_in_title","avg_words_freq_title","num_unique_words_title","unique_words_to_words_title_ratio","stdev_num_words_title_text","first_rev","only_rev","brand_names_in_text","polarity_text")

## Subtituting NAs & Inf with 0's
for(x in seq(1,ncol(df_dataset))){
  df_dataset[!is.finite(df_dataset[,x]),x]<-0 
}

num_cat_featuresIncLabel <- 6
num_cont_features <- ncol(df_dataset)-num_cat_featuresIncLabel
for(i in 1:num_cont_features){
  df_dataset[,i] <- as.double(as.character(df_dataset[,i]))
}

for(i in (num_cont_features+1):ncol(df_dataset)){
  df_dataset[,i] <- as.factor(df_dataset[,i])
}

####Read Model
model <- readRDS("data/model/poisb_mod_private_exp2.rds")
predicted <- predict(model,df_dataset,type = "response",n.trees = 30)
cutoff <- 0.5982485
predicted[predicted>=cutoff] <- 1
predicted[predicted<cutoff] <- 0
predicted <- as.factor(predicted)
levels(predicted) <- c("Spam","Normal")
dataset$predicted <- predicted
df_dataset$predicted <- predicted
write_json(dataset[,-10],paste("data/web_preview/",args[1],".json",sep = ""),pretty = TRUE)
write.csv(df_dataset,paste("data/dataset/",args[1],".csv",sep = ""),row.names = FALSE)
