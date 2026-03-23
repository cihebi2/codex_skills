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

data <- readr::read_file(paste0('demo_', '6758e7c8b309cfee57d3c676', '_', 'data1', '.txt'))
datas[['data1']] <- data

ngplotPostData <- list(
  account = 'cihebi',
  ngplotApiKey = '',
  template = '6758e7c8b309cfee57d3c676',
  data = datas,  
  arg = list(
    # params 
    nameCol = 'village' ,  
    valueCols = 'Chinese、Math、Physics、Chemistry' ,  
    sdCols = 'Chinese-std、Math-std、Physics-std、Chemistry-std' ,  
    step = '20' ,  
    yRange = '0,125;255,280' ,  
    xtitle = '' ,  
    ytitle = ''   
  )
)
NgplotApiFun(ngplotPostData, 'test')
