struct Preset{
  std::string message;
  std::string fgColour;
  std::string bgColour;
};

struct Presets {
  Preset unclassified = {
    "UNCLASSIFIED",
    "#FFFFFF",
    "#007a33"
  };
  Preset cui = {
    "CUI",
    "#FFFFFF",
    "#502b85"
  };
  Preset confidential = {
    "CONFIDENTIAL",
    "#FFFFFF",
    "#0033a0"
  };
  Preset secret = {
    "SECRET",
    "#FFFFFF",
    "#c8102e"
  };
  Preset topSecret = {
    "TOP SECRET",
    "#000000",
    "#ff8c00"
  };
  Preset tsSCI = {
    "TOP SECRET//SCI",
    "#000000",
    "#fce83a"
  };
};

