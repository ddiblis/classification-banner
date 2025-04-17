#include <QLabel>
#include <QEvent>
#include <QEnterEvent>

class Banner {
  private:
    std::string style;
    std::string position;
    QScreen*& screen;
    std::string bgColour;
    std::string fgColour;
    std::string message;
    QLabel *banner;

    void _setStyle() {
      std::ostringstream styleOss;
      styleOss << "background-color: " << bgColour << "; color: " << fgColour << "; font-size: 12px;" << " font-weight:bold;";
      std::string formattedStyle = styleOss.str();
      QString qStyle = QString::fromStdString(formattedStyle);
      banner -> setStyleSheet(qStyle);
    }

    void _setGeometry() {
      //QRect screenGeometry = QGuiApplication::primaryScreen()->geometry();
      QRect screenGeometry = screen->geometry();
      int bannerHeight = 20;
      int screenWidth = screenGeometry.width();
      // Judge me only if you can do better
      int bannerWidth = style == "Modern" ? message == "CUI" ? screenWidth / 30 : screenWidth / 22 : screenWidth;
      int topOffset = style == "Modern" ? 45 : 25;
      int bottomOffset = style == "Modern" ? 45 : 0; 

      if (position == "top") {
        banner -> setGeometry(screenGeometry.left(), screenGeometry.top() + topOffset, bannerWidth, bannerHeight);
      } else {
	int rightX = screenGeometry.right() - bannerWidth;
        banner -> setGeometry(rightX, screenGeometry.bottom() - bannerHeight - bottomOffset, bannerWidth, bannerHeight);
      }
    }


    void _init() {
      QString qMessage = QString::fromStdString(message);
      banner = new QLabel(qMessage);

      _setStyle();

      banner -> setAlignment(Qt::AlignCenter);
      banner -> setWindowTitle("Classification Banner");
      banner -> setWindowFlags(
            	  Qt::FramelessWindowHint | 
            	  Qt::WindowStaysOnTopHint | 
            	  Qt::Tool | 
            	  Qt::BypassWindowManagerHint |
            	  Qt::WindowTransparentForInput
            	  );

      _setGeometry();
     
      banner -> show();
    }


  public:
    
    void close() {
      QTimer::singleShot(0, banner, &QLabel::close);
    }

    Banner(
	    std::string positionInput, 
	    QScreen*& screenInput,
	    std::string messageInput,
	    std::string bgColourInput,
	    std::string fgColourInput,
	    std::string styleInput 
	  ) :
	    style(styleInput), 
	    position(positionInput), 
	    screen(screenInput),
	    message(messageInput), 
	    bgColour(bgColourInput),
	    fgColour(fgColourInput),
	    banner(nullptr) {
	      _init();
	    }
};

