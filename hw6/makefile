# conventional variable for c++ compiler
CXX := g++

# conventional variable for C preprocessor
CPPFLAGS := 

# conventional variable for C++ compiler flags
CXXFLAGS := -O3 -std=c++11 -Wall -Wextra -Wconversion -pedantic

# conventional variable for linker flags
LDFLAGS := -ljpeg

TARGET := main
OBJS := hw6.o image.o main.o
INCS := hw6.hpp image.hpp
FILES := BoxBlur03.jpeg BoxBlur07.jpeg BoxBlur11.jpeg BoxBlur15.jpeg BoxBlur19.jpeg BoxBlur23.jpeg BoxBlur27.jpeg

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(LDFLAGS)

%.o: %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CPPFLAGS) $(CXXFLAGS)

# use .PHONY for targets that do not produce a file
.PHONY: clean
clean:
	rm -f $(OBJS) $(TARGET) $(FILES) *~

.PHONY: run
run: $(TARGET)
	./$(TARGET)
