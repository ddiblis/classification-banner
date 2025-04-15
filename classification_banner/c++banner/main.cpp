#include <QApplication>
#include <QLabel>
#include <QScreen>
#include <QTimer>
#include <sstream>
#include <vector>
#include <iostream>
#include <getopt.h>
#include <libconfig.h++>

using namespace std;
using namespace libconfig;

#include "presets.h"
#include "banner.h"

struct BannerConfig {
    string message = "CUI";
    string fgcolour = "#FFFFFF";
    string bgcolour = "#502b85";
    string style = "Modern";
};

BannerConfig configure(int argc, char *argv[]) {
    Presets P;
    Config conf;
    // Catch error but do not exit, the conf file should be optional since you can use flags for setting the banner settings
    try {
        conf.readFile("/etc/classification-banner/banner.conf");
    } catch (const FileIOException &fioex) {
        cerr << "Error reading the configuration file!" << endl;
    } catch (const ParseException &pex) {
        cerr << "Parse error at " << pex.getFile() << ":" << pex.getLine() << " - " << pex.getError() << endl;
    }

    BannerConfig bannerConfig;

    try {
        //const Setting &root = conf.getRoot();
        //const Setting &global = root["global"];
        //
        bannerConfig.message = conf.lookup("global.message").c_str();
        bannerConfig.fgcolour = conf.lookup("global.fgcolor").c_str();
        bannerConfig.bgcolour = conf.lookup("global.bgcolor").c_str();
        bannerConfig.style = conf.lookup("global.style").c_str();
    } 
    catch (const SettingNotFoundException &e) {
        cerr << "One or more settings are missing in the configuration file." << endl;
    }

    int opt;
    while ((opt = getopt(argc, argv, "M:F:B:S:uCcstT")) != -1) {
        switch (opt) {
            case 'M': bannerConfig.message = optarg; break;
            case 'F': bannerConfig.fgcolour = optarg; break;
            case 'B': bannerConfig.bgcolour = optarg; break;
            case 'S': bannerConfig.style = optarg; break;
            case 'u':
	      bannerConfig.message = P.unclassified.message;
	      bannerConfig.bgcolour = P.unclassified.bgColour; 
	      bannerConfig.fgcolour = P.unclassified.fgColour;
	    break;
            case 'C': 
	      bannerConfig.message = P.cui.message;
	      bannerConfig.bgcolour = P.cui.bgColour; 
	      bannerConfig.fgcolour = P.cui.fgColour;
	    break;
            case 'c': 
	      bannerConfig.message = P.confidential.message;
	      bannerConfig.bgcolour = P.confidential.bgColour; 
	      bannerConfig.fgcolour = P.confidential.fgColour;
	    break;
            case 's': 
	      bannerConfig.message = P.secret.message;
	      bannerConfig.bgcolour = P.secret.bgColour; 
	      bannerConfig.fgcolour = P.secret.fgColour;
	    break;
            case 't': 
	      bannerConfig.message = P.topSecret.message;
	      bannerConfig.bgcolour = P.topSecret.bgColour; 
	      bannerConfig.fgcolour = P.topSecret.fgColour;
	    break;
            case 'T': 
	      bannerConfig.message = P.tsSCI.message;
	      bannerConfig.bgcolour = P.tsSCI.bgColour; 
	      bannerConfig.fgcolour = P.tsSCI.fgColour;
	    break;
            default: cerr << "Invalid argument!" << endl; exit(1);
        }
    }

    return bannerConfig;
}

int main(int argc, char *argv[]) {
  BannerConfig bannerConfig = configure(argc, argv);
  qputenv("QT_QPA_PLATFORM", QByteArray("xcb"));
  QApplication app(argc, argv);
  //std::vector<Banner> banners(10);

  //app.screens();
  Banner topBanner("top", bannerConfig.message, bannerConfig.bgcolour, bannerConfig.fgcolour, bannerConfig.style);
  Banner bottomBanner("bottom", bannerConfig.message, bannerConfig.bgcolour, bannerConfig.fgcolour, bannerConfig.style);
  return app.exec();
}
