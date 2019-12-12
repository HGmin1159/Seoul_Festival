library(plumber)
library(DBI)
library(RSQLite)
library(tidyverse)
library(pool)

con <- dbPool(RSQLite::SQLite(), dbname="SEOUL_FESTIVAL.db")


#* @filter cors
cors <- function(req, res) {
  
  res$setHeader("Access-Control-Allow-Origin", "*")
  
  if (req$REQUEST_METHOD == "OPTIONS") {
    res$setHeader("Access-Control-Allow-Methods","*")
    res$setHeader("Access-Control-Allow-Headers", req$HTTP_ACCESS_CONTROL_REQUEST_HEADERS)
    res$status <- 200 
    return(list())
  } else {
    plumber::forward()
  }
  
}



#* @serializer contentType list(type="application/json")
#* @param id
#* @get /restaurants
function(id) {
  qry <- sqlInterpolate(con, "SELECT *
                                FROM (SELECT *
                                        FROM festival_restaurant
                                        WHERE festival_id = ?id ) AS fr
                                JOIN restaurant_info AS r
                                ON fr.restaurants_id = r.id
                                ORDER BY distance;",
                        id=id)
  resjson = dbGetQuery(con, qry) %>% filter(x > 0) %>% jsonlite::toJSON(digits=NA)
  return (resjson)
}
