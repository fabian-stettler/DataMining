const constants = {
    //File Paths
    FILE_PATH_LOG_SUCCESSFULL: '/usr/src/datamining/logFiles/logFile.txt',
    FILE_PATH_LOG_ERROR: '/usr/src/datamining/logFiles/logFileError.txt',
    FILE_PATH_LOG_NO_ARTICLE: '/usr/src/datamining/logFiles/logFileNoArticle.txt',
    TARGET_DIR: "",
    FILE_PATH_LOG_TEMP: '/usr/src/datamining/logFiles/logFileTemp.txt',
    OUTPUT_DIR: "/usr/src/datamining/htmlFiles",
    FILE_PATH_ALREADY_SAVED_ARTICLES: "/usr/src/datamining/htmlFiles/savedArticles.txt",
    FILE_PATH_SUMMARY: "/usr/src/datamining/logFiles/logFileSummary.txt",

    //other
    URLS_TO_IGNORE : ["https://www.srf.ch/meteo/wetter"],
    NEW_ARTICLES : [],
};

module.exports = constants;