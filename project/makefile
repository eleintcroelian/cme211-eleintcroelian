CXX := g++
CXXFLAGS := -O3 -Wall -Wextra -Wconversion -std=c++11
RM := -rm

TARGET := main
OBJS := main.o matvecops.o COO2CSR.o CGSolver.o
INCS := matvecops.hpp COO2CSR.hpp CGSolver.hpp

$(TARGET): $(OBJS)
	$(CXX) -o $(TARGET) $(OBJS)

# this is a make pattern rule
%.o: %.cpp $(INCS)
	$(CXX) -c -o $@ $< $(CXXFLAGS)

.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)