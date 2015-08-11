###########################################################################################
# This script calculates statistic features about tags and datasets from open data portals.
###########################################################################################

close all; clear all;

#####################################
# 1. Load TAGS ######################
#####################################
function load_tags()
	filename = "tags.csv";
	sep = ";";

	file = fopen (filename, "r");

	#structure initialization
	tag.portal = "init";
	tag.name = "init";
	tag.count = 0;
	tag(66758).portal = "init"; 

	tline = fgetl(file);
	n = 1
	while ischar(tline)
		tag_arr = strsplit(tline,sep);
		tag(n).portal = tag_arr(1);
		tag(n).name = tag_arr(2);
		tag(n).count = tag_arr(3);
		tline = fgetl(file);
		n +=1 ;
	end

	fclose(file)
	save tag.mat tag
end

#####################################
# 2. Calculate Stats ################
#####################################

function load_portals()
	#find different portals
	load tag
	portals(1).url = tag(1).portal;
	for n = 1:length(tag)
		exists = false
		for k = 1:length(portals) 		
			if strcmp(tag(n).portal,char(portals(k).url))
				exists = true;
				break;
			end		
		end
		if (exists == false)
			portals(length(portals)+1).url = tag(n).portal;
		end
	end
	save portals.mat portals
end

function load_unique_tags()
	load tag
	unique_tags(1).name = tag(1).name;
	for n = 1:length(tag)
		exists = false
		for k = 1:length(unique_tags) 		
			if strcmp(tag(n).name,char(unique_tags(k).name))
				exists = true;
				break;
			end		
		end
		if (exists == false)
			unique_tags(length(unique_tags)+1).url = tag(n).name;
		end
	end
	save unique_tags.mat unique_tags
end

#####################################
# 3. Plot Percentage Over N #########
#####################################

figure()

subplot(2,2,1)
percentage_over_1
plot(100*sort(tags_over_n(:,2)))
title('% of tags used more than once')
axis([1 68 0 100])
xlabel('Open Data Portals index')

subplot(2,2,2)
percentage_over_2
plot(100*sort(tags_over_n(:,2)))
axis([1 68 0 100])
title('% of tags used more than twice')
xlabel('Open Data Portals index')

subplot(2,2,3)
percentage_over_3
plot(100*sort(tags_over_n(:,2)))
axis([1 68 0 100])
title('% of tags used more than three times')
xlabel('Open Data Portals index')

subplot(2,2,4)
percentage_over_4
plot(100*sort(tags_over_n(:,2)))
axis([1 68 0 100])
title('% of tags used more than four times')
xlabel('Open Data Portals index')
#number_of_portals = length(portals)
#number_of_tags = length(tag)
#number_of_different_tags = 
#number_of_datasets












