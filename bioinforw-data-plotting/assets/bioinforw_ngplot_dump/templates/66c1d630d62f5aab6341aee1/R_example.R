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

data <- readr::read_file(paste0('demo_', '66c1d630d62f5aab6341aee1', '_', 'data1', '.txt'))
datas[['data1']] <- data

data <- readr::read_file(paste0('demo_', '66c1d630d62f5aab6341aee1', '_', 'data2', '.txt'))
datas[['data2']] <- data

ngplotPostData <- list(
  account = 'cihebi',
  ngplotApiKey = '',
  template = '66c1d630d62f5aab6341aee1',
  data = datas,  
  arg = list(
    # params 
    groupCol = 'group' ,  
    xVCol = 'x' ,  
    yVCol = 'y' ,  
    linex1VCol = 'x1' ,  
    liney1VCol = 'y1' ,  
    linex2VCol = 'x2' ,  
    liney2VCol = 'y2'   
  )
)
NgplotApiFun(ngplotPostData, 'test')
