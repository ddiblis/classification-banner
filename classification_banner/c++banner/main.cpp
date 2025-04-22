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

//struct Test {
//  BannerConfig tes = {
//    "TEST",
//  };
//};

BannerConfig configure(int argc, char *argv[]) {
    Presets P;
    Config conf;
    // Catch error but do not exit, the conf file should be optional since you can use flags for setting the banner settings
    try {
      conf.readFile("/etc/classification-banner/banner.conf");
    } catch (const FileIOException &fioex) {
      cerr << "Config file not present, falling back on defaults" << endl;
    } catch (const ParseException &pex) {
      cerr << "Parse error at " << pex.getFile() << ":" << pex.getLine() << " - " << pex.getError() << endl;
    }

    BannerConfig bannerConfig;

    try {
      bannerConfig.message = conf.lookup("message").c_str();
      bannerConfig.fgcolour = conf.lookup("fgcolor").c_str();
      bannerConfig.bgcolour = conf.lookup("bgcolor").c_str();
      bannerConfig.style = conf.lookup("style").c_str();
    } 
    catch (const SettingNotFoundException &e) {
      cerr << "One or more config is not present, those will be defaulted" << endl;
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

void createBanners(std::vector<Banner*>& banners, QScreen* screen, BannerConfig& bannerConfig) {
banners.push_back(new Banner(
                        "top", 
                        screen, 
                        bannerConfig.message, 
                        bannerConfig.bgcolour, 
                        bannerConfig.fgcolour, 
                        bannerConfig.style
                      ));
banners.push_back(new Banner(
  		      "bottom", 
  	              screen, 
  	              bannerConfig.message, 
  	              bannerConfig.bgcolour, 
  	              bannerConfig.fgcolour, 
  	              bannerConfig.style
  		    ));
}

int main(int argc, char *argv[]) {
   BannerConfig bannerConfig = configure(argc, argv);
   qputenv("QT_QPA_PLATFORM", QByteArray("xcb"));
   QApplication app(argc, argv);
   std::vector<Banner*> allBanners;
   auto clearAllBanners = [&]() {
       for (Banner* b : allBanners) {
           b->close();
           delete b;
       }
       allBanners.clear();
       allBanners.shrink_to_fit();
   };
   auto rebuildAllBanners = [&]() {
       clearAllBanners();
       for (QScreen* screen : app.screens()) {
           createBanners(allBanners, screen, bannerConfig);
       }
   };
   rebuildAllBanners();
   for (QScreen* screen : app.screens()) {
     QObject::connect(screen, &QScreen::geometryChanged,
       [screen, &rebuildAllBanners]() {
         QTimer::singleShot(5000, rebuildAllBanners);
       });
   }

   QObject::connect(&app, &QGuiApplication::screenAdded,
     [&rebuildAllBanners]() {
       QTimer::singleShot(15000, rebuildAllBanners);
     });
   
   QObject::connect(&app, &QGuiApplication::screenRemoved,
     [&rebuildAllBanners]() {
       QTimer::singleShot(15000, rebuildAllBanners);
     });

   return app.exec();
}

