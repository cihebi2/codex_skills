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

data <- readr::read_file(paste0('demo_', '66b9b1dc0ca340783fc398c0', '_', 'data1', '.txt'))
datas[['data1']] <- data

data <- readr::read_file(paste0('demo_', '66b9b1dc0ca340783fc398c0', '_', 'data2', '.txt'))
datas[['data2']] <- data

ngplotPostData <- list(
  account = 'cihebi',
  ngplotApiKey = '',
  template = '66b9b1dc0ca340783fc398c0',
  data = datas,  
  arg = list(
    # params 
    nameCol = 'name' ,  
    groupCol = 'group' ,  
    minVCol = 'Min' ,  
    q1VCol = 'Q1' ,  
    midVCol = 'Q2' ,  
    q3VCol = 'Q3' ,  
    maxVCol = 'Max' ,  
    bigVCol = 'split1New' ,  
    name2Col = 'name' ,  
    yminV = '-50' ,  
    ymaxV = '10' ,  
    ystep = '10' ,  
    smallVcol = 'split0New' ,  
    ytitle = ''   
  )
)
NgplotApiFun(ngplotPostData, 'test')
