library(httr)
library(jsonlite)

NgplotApiFun <- function(ngplotPostData, svgOutName){
    json_data <- toJSON(ngplotPostData, auto_unbox = TRUE) 
    response <- POST(
        url = "https://www.bioinforw.com/ldm/ngplotApiSim/",
        body = list(data = json_data),
        encode = "form"
    )
    if(status_code(response) == 200){
        response_json <- fromJSON(content(response, "text"))
        if(response_json$code == 200){
            write(response_json$svg, file = paste0(svgOutName, ".svg"))  
            cat('Success, the result file is ', paste0(svgOutName , '.svg'))
        }else{
            cat(response_json$msg, "\n")  
        }
    }else{
        cat("HTTP ERROR:", status_code(response), "\n") 
    }
}


##Test:
datas <- list()

data <- readr::read_file(paste0('demo_', '6871c7c15a17bf5ffc87a104', '_', 'data1', '.txt'))
datas[['data1']] <- data

data <- readr::read_file(paste0('demo_', '6871c7c15a17bf5ffc87a104', '_', 'data2', '.txt'))
datas[['data2']] <- data

ngplotPostData <- list(
  account = 'cihebi',
  ngplotApiKey = '',
  template = '6871c7c15a17bf5ffc87a104',
  data = datas,  
  arg = list(
    # params 
    sourceCol = 'source	' ,  
    targetCol = 'target	' ,  
    valueCol = 'corr' ,  
    weightVCol = 'Weight' ,  
    rowCol = 'col' ,  
    colCol = 'row' ,  
    pVCol = 'pvalue' ,  
    maxv = 'auto' ,  
    pSection = '0.001、0.01、0.05' ,  
    weightSection = '0.1、0.3'   
  )
)
NgplotApiFun(ngplotPostData, 'test')
