CPP           = g++
HOME          = /home/roamware/kafka/testCppSource
THISDIR       = $(HOME)/testRepo/testCppKAfka
MAKEDIR       = $(HOME)/obj
BUILDDIR      = $(HOME)/bin
MAIN          = $(BUILDDIR)/testKafkaProducer
			     
RDKAFKAINC    = -I/usr/include/librdkafka

LIBRDKAFKA    = -L/usr/lib64/ -lrdkafka++


DFLAGS = -DPRODUCT_VERSION=\"1.0\" 
CFLAGS = -std=c++11

#OBJS =  $(patsubst $(THISDIR)/%.cpp,$(MAKEDIR)/%.o,$(wildcard $(THISDIR)/*.cpp))

FILES = $(wildcard $(THISDIR)/*.cpp)

DIRS = $(MAKEDIR) $(BUILDDIR) 

all: $(DIRS) $(MAIN) 

$(MAKEDIR):
	mkdir -p $(MAKEDIR) 
	
$(BUILDDIR):
	mkdir -p $(BUILDDIR) 	
	
$(MAIN): 
	$(CPP) $(CFLAGS) $(FILES) $(RDKAFKAINC) -o $(MAIN) $(LIBRDKAFKA)

clean:
	rm -rf $(MAKEDIR) $(MAIN) 

