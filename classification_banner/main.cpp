#include <QApplication>
#include <QLabel>
#include <QScreen>
#include <QTimer>

class Banner {
  private:
    std::string style;
    std::string position;

  public:
    Banner(std::string styleInput, std::string positionInput) {
      style = styleInput;
      position = positionInput;
    }

    void init() {
      QLabel banner("CUI");
      banner.setStyleSheet("background-color: #502b85; color: white; font-size: 15px;");
      banner.setAlignment(Qt::AlignCenter);
      banner.setWindowTitle("Classification Banner");
      banner.setWindowFlags(
            	  Qt::FramelessWindowHint | 
            	  Qt::WindowStaysOnTopHint | 
            	  Qt::Tool | 
            	  Qt::BypassWindowManagerHint | 
            	  Qt::WindowTransparentForInput
            	  );
      
      QRect screenGeometry = QGuiApplication::primaryScreen()->geometry();
      int bannerHeight = 20;
      int screenWidth = screenGeometry.width();
      int bannerWidth = style == "modern" ? screenWidth / 30 : screenWidth;
      int topOffset = style == "modern" ? 45 : 25;
      if (position == "top") {
        banner.setGeometry(0, 0 + topOffset, bannerWidth, bannerHeight);
      } else {
        banner.setGeometry(50, 50, bannerWidth, bannerHeight);
      }
      banner.show();
    }
};

int main(int argc, char *argv[]) {
  qputenv("QT_QPA_PLATFORM", QByteArray("xcb"));
  QApplication app(argc, argv);
  //std::string style = "modern";
  std::string style = "classic";


  Banner topBanner(style, "top");
  Banner bottomBanner(style, "bottom");
  return app.exec();
}
