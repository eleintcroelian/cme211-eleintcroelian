# conventional variable for c++ compiler
CXX := g++

# conventional variable for C preprocessor
CPPFLAGS :=

# conventional variable for C++ compiler flags
CXXFLAGS := -O3 -std=c++11 -Wall -Wextra -Wconversion

# conventional variable for linker flags
LDFLAGS := 

TARGET := main
OBJS := main.o matvecops.o COO2CSR.o heat.o sparse.o CGSolver.o
INCS := matvecops.hpp COO2CSR.hpp heat.hpp sparse.hpp CGSolver.hpp

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS) $(LDFLAGS)

%.o: %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CPPFLAGS) $(CXXFLAGS)

# use .PHONY for targets that do not produce a file
.PHONY: clean
clean:
	rm -f $(OBJS) $(TARGET) *~ output*

.PHONY: run
run: $(TARGET)
	./$(TARGET) input2.txt output_2_
