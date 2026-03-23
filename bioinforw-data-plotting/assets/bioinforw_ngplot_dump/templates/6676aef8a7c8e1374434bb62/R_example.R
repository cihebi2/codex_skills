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

data <- readr::read_file(paste0('demo_', '6753a1eaa9a528dc30e3977e', '_', 'data1', '.txt'))
datas[['data1']] <- data

ngplotPostData <- list(
  account = 'cihebi',
  ngplotApiKey = '',
  template = '6753a1eaa9a528dc30e3977e',
  data = datas,  
  arg = list(
    # params 
    nameCol = 'name' ,  
    valueColss = 'A、D;B、C、E'   
  )
)
NgplotApiFun(ngplotPostData, 'test')
