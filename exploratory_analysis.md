First we read the data and define the names of new variables created,
which are:

Explanatory: \* father\_involvement \* father\_presence \* num\_partners
\* num\_cohab\_biof \* num\_cohab\_anyp

Control: \* mothers\_education \* fathers\_education \* num\_cidi\_cases
\* hh\_income \* kid\_punished

    library(ggplot2)
    library(gridExtra)
    library(dplyr)

    ## 
    ## Attaching package: 'dplyr'

    ## The following object is masked from 'package:gridExtra':
    ## 
    ##     combine

    ## The following objects are masked from 'package:stats':
    ## 
    ##     filter, lag

    ## The following objects are masked from 'package:base':
    ## 
    ##     intersect, setdiff, setequal, union

    library(stargazer)

    ## 
    ## Please cite as:

    ##  Hlavac, Marek (2015). stargazer: Well-Formatted Regression and Summary Statistics Tables.

    ##  R package version 5.2. http://CRAN.R-project.org/package=stargazer

    df <- read.csv('FFChallenge/final_data.csv',header = T, stringsAsFactors = F)
    features <- c('father_involvement', 'father_presence', 'num_partners', 'num_cohab_biof', 'num_cohab_anyp','mothers_education', 'fathers_education', 'num_cidi_cases', 'hh_income', 'kid_punished')
    outcomes <- c('gpa', 'grit')
    head(df[features])

    ##   father_involvement father_presence num_partners num_cohab_biof
    ## 1             medium            high            0              3
    ## 2               high            high            0              4
    ## 3             medium          medium            1              2
    ## 4               high            high            0              4
    ## 5             medium          medium            1              0
    ## 6             medium          medium            4              0
    ##   num_cohab_anyp mothers_education fathers_education num_cidi_cases
    ## 1              3                 3                 1              0
    ## 2              4                 2                 2              1
    ## 3              3                 1                 1              1
    ## 4              4                 3                 3              0
    ## 5              2                 2                 2              0
    ## 6              1                 1                 1              0
    ##   hh_income kid_punished
    ## 1 10.977241            4
    ## 2 10.293178            0
    ## 3 10.049756            2
    ## 4 10.518804            4
    ## 5  9.261535            2
    ## 6  9.572205            2

Recode factors in a logical sequence:
=====================================

    df$father_involvement <- factor(df$father_involvement, levels=c("low","medium","high") )
    df$father_presence <- factor(df$father_presence, levels=c("low","medium","high"))

Data Checks:
============

-   missin values

<!-- -->

    apply(df[c(features,outcomes)],2,function(x) sum(is.na(x)))

    ## father_involvement    father_presence       num_partners 
    ##                  0                  0                  0 
    ##     num_cohab_biof     num_cohab_anyp  mothers_education 
    ##                  0                  0                  0 
    ##  fathers_education     num_cidi_cases          hh_income 
    ##                  0                  0                  0 
    ##       kid_punished                gpa               grit 
    ##                  0                  0                  0

The summary shows everything looks good.

    summary(df[c(features,outcomes)])

    ##  father_involvement father_presence  num_partners   num_cohab_biof 
    ##  low   :319         low   :132      Min.   :0.000   Min.   :0.000  
    ##  medium:244         medium:379      1st Qu.:0.000   1st Qu.:0.000  
    ##  high  :386         high  :438      Median :1.000   Median :2.000  
    ##                                     Mean   :1.176   Mean   :1.909  
    ##                                     3rd Qu.:2.000   3rd Qu.:4.000  
    ##                                     Max.   :8.000   Max.   :4.000  
    ##  num_cohab_anyp  mothers_education fathers_education num_cidi_cases  
    ##  Min.   :0.000   Min.   :1.000     Min.   :1.000     Min.   :0.0000  
    ##  1st Qu.:1.000   1st Qu.:1.000     1st Qu.:1.000     1st Qu.:0.0000  
    ##  Median :3.000   Median :2.000     Median :2.000     Median :0.0000  
    ##  Mean   :2.433   Mean   :2.228     Mean   :2.165     Mean   :0.3404  
    ##  3rd Qu.:4.000   3rd Qu.:3.000     3rd Qu.:3.000     3rd Qu.:0.0000  
    ##  Max.   :4.000   Max.   :4.000     Max.   :4.000     Max.   :4.0000  
    ##    hh_income       kid_punished         gpa            grit      
    ##  Min.   : 7.101   Min.   : 0.000   Min.   :1.00   Min.   :1.750  
    ##  1st Qu.: 9.684   1st Qu.: 0.000   1st Qu.:2.50   1st Qu.:3.000  
    ##  Median :10.195   Median : 1.000   Median :3.00   Median :3.500  
    ##  Mean   :10.212   Mean   : 1.703   Mean   :2.88   Mean   :3.443  
    ##  3rd Qu.:10.785   3rd Qu.: 3.000   3rd Qu.:3.50   3rd Qu.:4.000  
    ##  Max.   :11.708   Max.   :12.000   Max.   :4.00   Max.   :4.000

Grit and GPA histograms:

    # hist(df$grit)
    ggplot(data=df)+
      geom_histogram(aes(x=gpa),bins=10, fill="maroon")+
      xlab("GPA at Age 15") +
      ylab("Count")+
      ggtitle("Histogram of GPA") + theme(plot.title = element_text(hjust = 0.5))

<img src="exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-6-1.png" style="display: block; margin: auto;" />
Get correlation coefficients:

Correaltion between gpa and grit:

    cor(df$gpa,df$grit)

    ## [1] 0.2070167

Though small magnitudes, we see -ve correlation in num\_cidi\_cases,
num\_partners and kid\_punished and +ve otherwise as expected.

    print('Correlation with GPA:')

    ## [1] "Correlation with GPA:"

    apply(df[features[3:length(features)]],2,function(x) cor(x,y=df$gpa))

    ##      num_partners    num_cohab_biof    num_cohab_anyp mothers_education 
    ##       -0.18270138        0.23879478        0.21620022        0.30556781 
    ## fathers_education    num_cidi_cases         hh_income      kid_punished 
    ##        0.31313510       -0.10390097        0.29916649       -0.01886756

    print('Correlation with Grit:')

    ## [1] "Correlation with Grit:"

    apply(df[features[3:length(features)]],2,function(x) cor(x,y=df$grit))

    ##      num_partners    num_cohab_biof    num_cohab_anyp mothers_education 
    ##        0.05639726       -0.08507627       -0.04707836       -0.11191825 
    ## fathers_education    num_cidi_cases         hh_income      kid_punished 
    ##       -0.05759943       -0.05781087       -0.10875741       -0.03932128

Make histograms for all variables:

    for (col in features[3:length(features)]) {
      hist(df[,col])
    }

![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-9-1.png)![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-9-2.png)![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-9-3.png)![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-9-4.png)![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-9-5.png)![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-9-6.png)![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-9-7.png)![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-9-8.png)
Make bar chart for father's involvement and presence:

    plot1 <- ggplot(data=df) +
      geom_bar(aes(x=father_involvement)) +
      ylab("Count")
     plot2 <- ggplot(data=df) +
      geom_boxplot(aes(x=father_involvement, y=gpa)) +
       ylab("GPA at Age 15")
    grid.arrange(plot1, plot2, ncol=2, top="Father's Involvement Feature")

![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-10-1.png)
Tabulate presence and involvement:

    table(df$father_involvement, df$father_presence)

    ##         
    ##          low medium high
    ##   low    125    183   11
    ##   medium   7    166   71
    ##   high     0     30  356

Make boxplots for father's involvement:

    plot1 <- ggplot(data=df) +
      geom_bar(aes(x=father_presence)) +
      ylab("Count")
     plot2 <- ggplot(data=df) +
      geom_boxplot(aes(x=father_presence, y=gpa)) +
       ylab("GPA at Age 15")
    grid.arrange(plot1, plot2, ncol=2, top="Father's Presence Feature")

![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-12-1.png)
Though the boxplots are highly overlapping, we can see that father's
involvement has a slightly positive impact on GPA. Probably there are
many confounding factors which we'll take into consideration in the
linear models.

Run a 2-sample t-test:

    fit <- aov(gpa~father_involvement,data=df)
    summary(fit)

    ##                     Df Sum Sq Mean Sq F value   Pr(>F)    
    ## father_involvement   2   23.4  11.716   27.14 3.46e-12 ***
    ## Residuals          946  408.4   0.432                     
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

    fit <- aov(gpa~father_presence,data=df)
    summary(fit)

    ##                  Df Sum Sq Mean Sq F value   Pr(>F)    
    ## father_presence   2   21.4  10.680   24.62 3.79e-11 ***
    ## Residuals       946  410.4   0.434                     
    ## ---
    ## Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

    # plot(fit)
    # TukeyHSD(fit)

Anove gives a highly significant result because it tests that the 3
means are equal. But its a good to compare pairs as well to see which
one is actually different. As shown by the boxplot, out hypothesis is
confirmed that

Make boxplots for father's involvement on grit:

    plot1 <- ggplot(data=df) +
      geom_boxplot(aes(x=father_involvement, y=grit)) 
    plot2 <- ggplot(data=df) +
      geom_boxplot(aes(x=father_presence, y=grit)) 
    grid.arrange(plot1, plot2, ncol=2)

![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-14-1.png)

plot others

    plot1 <- ggplot(data=df) +
      geom_bar(aes(x=num_cohab_biof)) +
      ylab("Count") + xlab("#Cohabiting with Biological Father")
    plot2 <- ggplot(data=df) +
      geom_bar(aes(x=num_cohab_anyp)) +
      ylab("Count") + xlab("#Cohabiting with Any Partner")
    grid.arrange(plot1, plot2, ncol=2, top="Presence of a Fatherly Figure")

![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-15-1.png)

    ggplot(data=df) +
      geom_bar(aes(x=num_partners)) +
      ylab("Count") + xlab("#Number of Relationships With Partners Other than Father")

![](exploratory_analysis_files/figure-markdown_strict/unnamed-chunk-16-1.png)

Linear Models:
==============

we'll start with father's presence and then keep adding new variables in
the model:

    lm1 <- lm(gpa~father_presence,data=df)
    # summary(lm1)
    lm2 <- lm(gpa~num_cohab_biof+father_presence,data=df)
    # summary(lm2)
    stargazer(lm1,lm2,type="text",report = "vcp*",intercept.bottom = F, omit.stat=c("adj.rsq","ser","f"))

    ## 
    ## ==================================================
    ##                           Dependent variable:     
    ##                       ----------------------------
    ##                                   gpa             
    ##                             (1)           (2)     
    ## --------------------------------------------------
    ## Constant                   2.714         2.707    
    ##                        p = 0.000***   p = 0.000***
    ##                                                   
    ## num_cohab_biof                           0.083    
    ##                                       p = 0.006***
    ##                                                   
    ## father_presencemedium      0.037         -0.008   
    ##                          p = 0.576     p = 0.903  
    ##                                                   
    ## father_presencehigh        0.328         0.040    
    ##                       p = 0.00000***   p = 0.743  
    ##                                                   
    ## --------------------------------------------------
    ## Observations                949           949     
    ## R2                         0.049         0.057    
    ## ==================================================
    ## Note:                  *p<0.1; **p<0.05; ***p<0.01

lm2 shows that father\_presence is not important in presence of
num\_cohab\_biof which is also a proxy for the same. so we'll just keep
one of them.

    lm3 <- lm(gpa~num_cohab_biof + father_presence  + father_involvement, data=df)
    lm4 <- lm(gpa~num_cohab_biof + father_involvement, data=df)
    stargazer(lm2,lm3,lm4,type="text",report = "vcp*",intercept.bottom = F, omit.stat=c("adj.rsq","ser","f"))

    ## 
    ## ===============================================================
    ##                                   Dependent variable:          
    ##                          --------------------------------------
    ##                                           gpa                  
    ##                              (1)          (2)          (3)     
    ## ---------------------------------------------------------------
    ## Constant                    2.707        2.704        2.678    
    ##                          p = 0.000*** p = 0.000*** p = 0.000***
    ##                                                                
    ## num_cohab_biof              0.083        0.063        0.058    
    ##                          p = 0.006*** p = 0.043**  p = 0.006***
    ##                                                                
    ## father_presencemedium       -0.008       -0.046                
    ##                           p = 0.903    p = 0.531               
    ##                                                                
    ## father_presencehigh         0.040        -0.058                
    ##                           p = 0.743    p = 0.653               
    ##                                                                
    ## father_involvementmedium                 0.086        0.071    
    ##                                        p = 0.182    p = 0.235  
    ##                                                                
    ## father_involvementhigh                   0.195        0.181    
    ##                                       p = 0.024**  p = 0.026** 
    ##                                                                
    ## ---------------------------------------------------------------
    ## Observations                 949          949          949     
    ## R2                          0.057        0.062        0.062    
    ## ===============================================================
    ## Note:                               *p<0.1; **p<0.05; ***p<0.01

Add more:

    df$num_cohab_anyp2 <- df$num_cohab_anyp - df$num_cohab_biof
    lm5 <- lm(gpa~num_cohab_biof + father_involvement + num_cohab_anyp2, data=df)
    stargazer(lm4,lm5,type="text",report = "vcp*",intercept.bottom = F, omit.stat=c("adj.rsq","ser","f"))

    ## 
    ## =====================================================
    ##                              Dependent variable:     
    ##                          ----------------------------
    ##                                      gpa             
    ##                               (1)            (2)     
    ## -----------------------------------------------------
    ## Constant                     2.678          2.641    
    ##                           p = 0.000***  p = 0.000*** 
    ##                                                      
    ## num_cohab_biof               0.058          0.063    
    ##                           p = 0.006***  p = 0.003*** 
    ##                                                      
    ## father_involvementmedium     0.071          0.081    
    ##                            p = 0.235      p = 0.183  
    ##                                                      
    ## father_involvementhigh       0.181          0.198    
    ##                           p = 0.026**    p = 0.017** 
    ##                                                      
    ## num_cohab_anyp2                             0.033    
    ##                                           p = 0.220  
    ##                                                      
    ## -----------------------------------------------------
    ## Observations                  949            949     
    ## R2                           0.062          0.063    
    ## =====================================================
    ## Note:                     *p<0.1; **p<0.05; ***p<0.01

    lm6 <- lm(gpa~num_cohab_biof + father_involvement + num_cohab_anyp + num_partners, data=df)
    stargazer(lm5,lm6,type="text",report = "vcp*",intercept.bottom = F, omit.stat=c("adj.rsq","ser","f"))

    ## 
    ## =====================================================
    ##                              Dependent variable:     
    ##                          ----------------------------
    ##                                      gpa             
    ##                               (1)            (2)     
    ## -----------------------------------------------------
    ## Constant                     2.641          2.680    
    ##                           p = 0.000***  p = 0.000*** 
    ##                                                      
    ## num_cohab_biof               0.063          0.020    
    ##                           p = 0.003***    p = 0.539  
    ##                                                      
    ## father_involvementmedium     0.081          0.081    
    ##                            p = 0.183      p = 0.180  
    ##                                                      
    ## father_involvementhigh       0.198          0.190    
    ##                           p = 0.017**    p = 0.022** 
    ##                                                      
    ## num_cohab_anyp2              0.033                   
    ##                            p = 0.220                 
    ##                                                      
    ## num_cohab_anyp                              0.035    
    ##                                           p = 0.195  
    ##                                                      
    ## num_partners                               -0.019    
    ##                                           p = 0.376  
    ##                                                      
    ## -----------------------------------------------------
    ## Observations                  949            949     
    ## R2                           0.063          0.064    
    ## =====================================================
    ## Note:                     *p<0.1; **p<0.05; ***p<0.01

    # lm6 <- lm(gpa~mothers_education+fathers_education+num_cidi_cases+ hh_income+kid_punished,data=df)
    # summary(lm6)
    lm7 <- lm(gpa~num_cohab_biof + father_involvement + num_cohab_anyp + num_partners +
                mothers_education+fathers_education+num_cidi_cases+ hh_income+kid_punished, data=df)
    stargazer(lm6,lm7,type="text",report = "vcp*",intercept.bottom = F, omit.stat=c("adj.rsq","ser","f"))

    ## 
    ## =====================================================
    ##                              Dependent variable:     
    ##                          ----------------------------
    ##                                      gpa             
    ##                               (1)           (2)      
    ## -----------------------------------------------------
    ## Constant                     2.680         1.642     
    ##                          p = 0.000***  p = 0.00000***
    ##                                                      
    ## num_cohab_biof               0.020         -0.007    
    ##                            p = 0.539     p = 0.830   
    ##                                                      
    ## father_involvementmedium     0.081         0.074     
    ##                            p = 0.180     p = 0.202   
    ##                                                      
    ## father_involvementhigh       0.190         0.123     
    ##                           p = 0.022**    p = 0.125   
    ##                                                      
    ## num_cohab_anyp               0.035         0.029     
    ##                            p = 0.195     p = 0.276   
    ##                                                      
    ## num_partners                -0.019         -0.011    
    ##                            p = 0.376     p = 0.586   
    ##                                                      
    ## mothers_education                          0.078     
    ##                                         p = 0.007*** 
    ##                                                      
    ## fathers_education                          0.105     
    ##                                        p = 0.0002*** 
    ##                                                      
    ## num_cidi_cases                             -0.045    
    ##                                          p = 0.110   
    ##                                                      
    ## hh_income                                  0.074     
    ##                                         p = 0.042**  
    ##                                                      
    ## kid_punished                               -0.012    
    ##                                          p = 0.267   
    ##                                                      
    ## -----------------------------------------------------
    ## Observations                  949           949      
    ## R2                           0.064         0.146     
    ## =====================================================
    ## Note:                     *p<0.1; **p<0.05; ***p<0.01

    lm8 <- lm(gpa~num_cohab_biof + father_involvement + num_cohab_anyp + num_partners +
                mothers_education+fathers_education+ hh_income, data=df)
    stargazer(lm7,lm8,type="text",report = "vcp*",intercept.bottom = F, omit.stat=c("adj.rsq","ser","f"))

    ## 
    ## ======================================================
    ##                               Dependent variable:     
    ##                          -----------------------------
    ##                                       gpa             
    ##                               (1)            (2)      
    ## ------------------------------------------------------
    ## Constant                     1.642          1.591     
    ##                          p = 0.00000*** p = 0.00001***
    ##                                                       
    ## num_cohab_biof               -0.007         -0.007    
    ##                            p = 0.830      p = 0.837   
    ##                                                       
    ## father_involvementmedium     0.074          0.076     
    ##                            p = 0.202      p = 0.194   
    ##                                                       
    ## father_involvementhigh       0.123          0.127     
    ##                            p = 0.125      p = 0.113   
    ##                                                       
    ## num_cohab_anyp               0.029          0.026     
    ##                            p = 0.276      p = 0.320   
    ##                                                       
    ## num_partners                 -0.011         -0.014    
    ##                            p = 0.586      p = 0.506   
    ##                                                       
    ## mothers_education            0.078          0.078     
    ##                           p = 0.007***   p = 0.007*** 
    ##                                                       
    ## fathers_education            0.105          0.107     
    ##                          p = 0.0002***  p = 0.0002*** 
    ##                                                       
    ## num_cidi_cases               -0.045                   
    ##                            p = 0.110                  
    ##                                                       
    ## hh_income                    0.074          0.076     
    ##                           p = 0.042**    p = 0.038**  
    ##                                                       
    ## kid_punished                 -0.012                   
    ##                            p = 0.267                  
    ##                                                       
    ## ------------------------------------------------------
    ## Observations                  949            949      
    ## R2                           0.146          0.143     
    ## ======================================================
    ## Note:                      *p<0.1; **p<0.05; ***p<0.01
