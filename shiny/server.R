library(shiny)
library(DBI)
library(RSQLite)
library(tidyverse)


fetch.res = function(fes.id) {
    con <- dbConnect(RSQLite::SQLite(), "SEOUL_FESTIVAL.db")
    qry <- sqlInterpolate(con, "SELECT *
                                FROM (SELECT *
                                        FROM festival_restaurant
                                        WHERE festival_id = ?id ) AS fr
                                JOIN restaurant_info AS r
                                ON fr.restaurants_id = r.id
                                ORDER BY distance;",
                          id=fes.id)
    resjson = dbGetQuery(con, qry) %>% filter(x > 0) %>% jsonlite::toJSON(digits=NA)
    dbDisconnect(con)
    return (resjson)
}

server <- function(input, output, session) {
    observeEvent(input$fesid, { session$sendCustomMessage('1', fetch.res(input$fesid)) })
}
