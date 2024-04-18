require(dplyr)
require(Hmisc)
require(rio)

cal_dm <- function(df, euculidean = F, method = 'spearman'){
  if(euculidean){
    output = (
      t(df) %>% # transpose to accommodate further munipulations
        dist() %>% # calculate euculidean distances
        as.vector()
    )
  } else {
    dm = 1 - rcorr(
      t(t(df)),
      type = method
      )$r
    output = dm[lower.tri(dm, diag = F)]
  }

  return(output)
}

cal_RSA <- function(v1, v2, method = 'spearman'){
  output = cor(
    v1, 
    v2,
    # specify the intented method in function parameters
    method = method
  ) %>% 
    atanh() %>% # normalize the result to Z dist space from F dist space
    round(., 4)
  
  return(output)
}

# Usage
# read files
df1 = import('period_a_rankings.xlsx')
row.names(df1) <- df1[,1]

df2 = import('period_b_rankings.xlsx')
row.names(df2) <- df2[,1]
# Call functions
cal_RSA(
  cal_dm(df1),
  cal_dm(df2)
)