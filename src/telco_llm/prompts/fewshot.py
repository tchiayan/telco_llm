database_few_shot = [
    {
        "input": "How is the performance 4G Volte Drop Call rate for site 1123A for past 1 weeks", 
        "query": "SELECT time , 100*sum(VOLTE_DROP_NUM)/sum(VOLTE_DROP_DENOM) `4G VoLTE Drop Call Rate` FROM `rf-oss.dailydata.mc4g_cell_combined` WHERE Date(time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) AND ( site = '1123A' ) GROUP BY time ORDER BY time"
    }, 
    {
        "input": "How is the performance 2G TCH Drop rate for site 1123A for past 1 month", 
        "query": "SELECT time , 100*sum(TCH_DROP_NUM)/sum(TCH_DROP_DENOM) `2G TCH Drop Rate` FROM `rf-oss.dailydata.mc2g_cell_combined` WHERE Date(time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) AND ( site = '1123A' ) GROUP BY time ORDER BY time"
    }, 
    {
        "input": "How much total 4G data download traffic for the site 1011A for past 2 week", 
        "query": "SELECT sum(LTE_DATA_TRAFFIC_GB) `4G Data Download Traffic` FROM `rf-oss.dailydata.mc4g_cell_combined` WHERE Date(time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY) AND ( site = '1011A' )"
    }, 
    {
        "input": "Which cell is having the worst performance 4G RRC setup success rate for 1011A in last 3 days", 
        "query": "SELECT object `Cell` , 100*sum(RRC_SETUP_NUM)/sum(RRC_SETUP_DENOM) `RRC Setup Success Rate` FROM `rf-oss.dailydata.mc4g_cell_combined` WHERE Date(time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 DAY) AND ( site = '1011A' ) GROUP BY object ORDER BY `RRC Setup Success Rate` LIMIT 1;"
    }
]