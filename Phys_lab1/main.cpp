#include <bits/stdc++.h>

class Point2D {
public:
  float x, y;
  bool isCorrectSystem;

  Point2D(float set_x, float set_y) {
    x = set_x;
    y = set_y;
    isCorrectSystem = true;
  }

  Point2D return_itself() { return Point2D(x, y); }

  Point2D rectangular_to_polar() {
    float r = sqrt(x * x + y * y);
    float phi;

    if (x > 0 && y >= 0) {
      phi = atan(y / x);
    } else if (x > 0 && y < 0) {
      phi = atan(y / x) + 2 * M_PI;
    } else if (x < 0) {
      phi = atan(y / x) + M_PI;
    } else if (x == 0 && y > 0) {
      phi = M_PI / 2;
    } else if (x == 0 && y < 0) {
      phi = -M_PI / 2;
    } else {
      std::cout << "x and y are equal to zero - WRONG";
      return return_itself();
    }

    return Point2D(r, phi);
  }

  Point2D polar_to_rectangular() {
    float new_x = x * cos(y * M_PI / 180);
    float new_y = x * sin(y * M_PI / 180);

    return Point2D(new_x, new_y);
  }

  Point2D detecting_system(std::string syst_to_switch,
                           std::string current_syst) {
    if (syst_to_switch == current_syst) {
      return return_itself();
    }
    if (syst_to_switch == "polar") {
      return rectangular_to_polar();
    }
    if (syst_to_switch == "rectangular") {
      return polar_to_rectangular();
    } else {
      std::cout << "Wrong system\n";
      isCorrectSystem = false;
      return return_itself();
    }
  }
};

class Point3D {

public:
  float x, y, z;
  bool isCorrectSystem;

  Point3D(float set_x, float set_y, float set_z) {
    x = set_x;
    y = set_y;
    z = set_z;
    isCorrectSystem = true;
  }

  Point3D rectangular_to_spherical() {                 // done
    float radius_vector = sqrt(x * x + y * y + z * z); // (x, y, z)
    float teta = acos(z / radius_vector);
    float phi = atan(y / x);

    return Point3D(radius_vector, teta, phi);
  }

  Point3D rectangular_to_cylindrical() { // done
    float p = sqrtf(x * x + y * y);
    float phi = atan(y / x);

    return Point3D(p, phi, z);
  }

  Point3D spherical_to_rectangular() { // done
    float new_x =
        x * sin(z * M_PI / 180) * cos(y * M_PI / 180); // (p, phi, teta)
    float new_y = x * sin(z * M_PI / 180) * sin(y * M_PI / 180);
    float new_z = x * cos(z * M_PI / 180);

    return Point3D(new_x, new_y, new_z);
  }
  Point3D spherical_to_cylindrical() { // done
    float r = x * sin(z * M_PI / 180); // (p, phi, teta)
    float phi = y;
    float new_z = x * cos(z * M_PI / 180);

    return Point3D(r, phi, new_z);
  }

  Point3D cylindrical_to_spherical() { // done
    float r = sqrt(x * x + z * z);     // (r, phi, z)
    float teta = y;
    float phi = atan(x / z);

    return Point3D(r, teta, phi);
  }

  Point3D cylindrical_to_rectangular() {   // done
    float new_x = x * cos(y * M_PI / 180); // (r, phi, z)
    float new_y = x * sin(y * M_PI / 180);
    float new_z = y;

    return Point3D(new_x, new_y, new_z);
  }

  Point3D return_itself() { return Point3D(x, y, z); }

  Point3D to_spherical(std::string current_system) {
    if (current_system == "cylindrical") {
      return cylindrical_to_spherical();
    } else if (current_system == "rectangular") {
      return rectangular_to_spherical();
    } else {
      std::cout << "Wrong current system\n";
      return return_itself();
    }
  }

  Point3D to_cylindrical(std::string current_system) {
    if (current_system == "spherical") {
      return spherical_to_cylindrical();
    } else if (current_system == "rectangular") {
      return rectangular_to_cylindrical();
    } else {
      std::cout << "Wrong current system\n";
      return return_itself();
    }
  }

  Point3D to_rectangular(std::string current_system) {
    if (current_system == "spherical") {
      return spherical_to_rectangular();
    } else if (current_system == "cylindrical") {
      return cylindrical_to_rectangular();
    } else {
      std::cout << "Wrong current system\n";
      isCorrectSystem = false;
      return return_itself();
    }
  }

  Point3D detecting_system(std::string system_to_switch,
                           std::string current_system) {
    if (system_to_switch == current_system) {
      return return_itself();
    } else if (system_to_switch == "spherical") {
      return to_spherical(current_system);
    } else if (system_to_switch == "cylindrical") {
      return to_cylindrical(current_system);
    } else if (system_to_switch == "rectangular") {
      return to_rectangular(current_system);
    } else {
      std::cout << "Wrong switching system\n";
      isCorrectSystem = false;
      return return_itself();
    }
  }
};

std::string toLower(std::string str) {
  transform(str.begin(), str.end(), str.begin(), ::tolower);
  return str;
}

float safeFloatInput(const std::string &prompt) {
  float value;
  while (true) {
    std::cout << prompt;
    if (!(std::cin >> value)) {
      std::cerr << "Not a number, try again.\n";
      std::cin.clear(); // Очистка флага ошибки
      std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
    } else {
      return value;
    }
  }
}

void for_three_dim() {
  std::cout << "Spherical (r, phi, teta)\nCylindrical (p, phi, z)\nRectangular "
               "(x, y, z)\n\n";

  std::cout << "Write coordinates:\n";
  float a = safeFloatInput("Enter first coordinate: ");
  float b = safeFloatInput("Enter second coordinate: ");
  float c = safeFloatInput("Enter third coordinate: ");

  Point3D point(a, b, c);

  std::cout << "What system do you use? (type quit to quit)\n";
  std::string current_system;
  std::cin >> current_system;

  current_system = toLower(current_system);

  if (current_system == "quit") {
    std::cout << "Bye\n";
    return;
  }

  std::cout << "What system do you want to switch?\n";
  std::string switch_to_syst;
  std::cin >> switch_to_syst;

  switch_to_syst = toLower(switch_to_syst);

  if (switch_to_syst == "quit") {
    std::cout << "Bye\n";
    return;
  }

  point = point.detecting_system(switch_to_syst, current_system);

  if (!point.isCorrectSystem) {
    return;
  }

  std::cout << "What's the rounding factor?\n";
  double rounding;
  std::cin >> rounding;

  if (switch_to_syst == "spherical") {
    std::cout << "(" << "r: " << std::setprecision(rounding) << std::fixed
              << point.x << ", " << "teta: " << std::setprecision(rounding)
              << std::fixed << point.y << ", "
              << "phi: " << std::setprecision(rounding) << std::fixed
              << point.z * 180 / M_PI << ")" << std::endl;
  }
  if (switch_to_syst == "cylindrical") {
    std::cout << "(" << "r: " << std::setprecision(rounding) << std::fixed
              << point.x << ", " << "phi: " << std::setprecision(rounding)
              << std::fixed << point.y << ", "
              << "z: " << std::setprecision(rounding) << std::fixed << point.z
              << ")" << std::endl;
  }
  if (switch_to_syst == "rectangular") {
    std::cout << "(" << "x: " << std::setprecision(rounding) << std::fixed
              << point.x << ", " << "y: " << std::setprecision(rounding)
              << std::fixed << point.y << ", "
              << "z: " << std::setprecision(rounding) << std::fixed << point.z
              << ")" << std::endl;
  }
}

void for_two_dim() {
  std::cout << "1. Polar (r, phi)\n2. Rectangular (x, y)\n\n";

  std::cout << "Write coordinates:\n";
  float a = safeFloatInput("Enter first coordinate: ");
  float b = safeFloatInput("Enter second coordinate: ");

  Point2D point(a, b);

  std::cout << "What system do you use? (type quit to quit)\n";
  std::string current_system;
  std::cin >> current_system;

  current_system = toLower(current_system);

  if (current_system == "quit") {
    std::cout << "Bye\n";
    return;
  }

  std::cout << "What system do you want to switch?\n";
  std::string switch_to_syst;
  std::cin >> switch_to_syst;

  switch_to_syst = toLower(switch_to_syst);

  if (switch_to_syst == "quit") {
    std::cout << "Bye\n";
    return;
  }

  point = point.detecting_system(switch_to_syst, current_system);

  if (!point.isCorrectSystem) {
    return;
  }

  std::cout << "What's the rounding factor?\n";
  double rounding;
  std::cin >> rounding;

  if (switch_to_syst == "polar") {
    std::cout << "(" << "r: " << std::setprecision(rounding) << std::fixed
              << point.x << ", " << "phi: " << std::fixed
              << std::setprecision(rounding) << point.y * 180 / M_PI << ")"
              << std::endl;
  }
  if (switch_to_syst == "rectangular") {
    std::cout << "(" << "x: " << std::setprecision(rounding) << std::fixed
              << point.x << ", " << "y: " << std::setprecision(rounding)
              << std::fixed << point.y << ")" << std::endl;
  }
}

int main() {
  std::cout << "2 or 3 dimensions?\n";
  short dims;
  std::cin >> dims;
  if (dims == 2) {
    for_two_dim();
  }
  if (dims == 3) {
    for_three_dim();
  }
  return 0;
}


