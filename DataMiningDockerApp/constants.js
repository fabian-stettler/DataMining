/**
 * Manages all file paths and other constants
 * @type {{OUTPUT_DIR: string, TARGET_DIR: string, FILE_PATH_LOG_TEMP: string, FILE_PATH_LOG_SUCCESSFULL: string, FILE_PATH_LOG_ERROR: string, FILE_PATH_LOG_NO_ARTICLE: string, NEW_ARTICLES: *[], FILE_PATH_SUMMARY: string, URLS_TO_IGNORE: string[], FILE_PATH_ALREADY_SAVED_ARTICLES: string, LOG_DIR: string}}
 */
const constants = {
    //File Paths
    FILE_PATH_LOG_SUCCESSFULL: '/usr/src/datamining/logFiles/logFile.txt',
    FILE_PATH_LOG_ERROR: '/usr/src/datamining/logFiles/logFileError.txt',
    FILE_PATH_LOG_ABORT_ERROR:'/usr/src/datamining/logFiles/logFileAbortError.txt',
    FILE_PATH_LOG_NO_ARTICLE: '/usr/src/datamining/logFiles/logFileNoArticle.txt',
    TARGET_DIR: "",
    FILE_PATH_LOG_TEMP: '/usr/src/datamining/logFiles/logFileTemp.txt',
    OUTPUT_DIR: "/usr/src/datamining/htmlFiles",
    LOG_DIR: '/usr/src/datamining/logFiles',
    FILE_PATH_ALREADY_SAVED_ARTICLES: "/usr/src/datamining/logFiles/savedArticles.txt",
    FILE_PATH_LAST_STATE: "/usr/src/datamining/logFiles/lastState.txt",
    FILE_PATH_SUMMARY: "/usr/src/datamining/logFiles/logFileSummary.txt",

    //other
    URLS_TO_IGNORE : ["https://www.srf.ch/meteo/wetter"],
    NEW_ARTICLES : [],
};

module.exports = constants;