tags_distibution;

for i = 1:length(tags_distibution)
	a = tags_distibution{i};
	perc_once(i) = sum(a==1)/(length(a)-sum(a==0));
end

h=figure(1);
hist(perc_once,0:0.1:1)
set(gca,'XTick',[0:.1:1])
set(gca,'XTickLabel',100*[0:.1:1])
axis([-0.1 1.2 0 26])
xlabel('% of tags used only once')
ylabel('Number of ODPs')

W = 4; H = 3;
set(h,'PaperUnits','inches')
set(h,'PaperOrientation','portrait');
set(h,'PaperSize',[H,W])
set(h,'PaperPosition',[0,0,W,H])

FN = findall(h,'-property','FontName');
set(FN,'FontName','/usr/share/fonts/dejavu/DejaVuSerifCondensed.ttf');
FS = findall(h,'-property','FontSize');
set(FS,'FontSize',8);

print(h,'-dpng','-color','~/ownCloud/Documents Cloud/Bonn/EIS/Papers/2016/ICSC_Semantic_Tagging/images/tag_once_dist.png')

##################

tags_perdataset;

for i = 1:length(tags_per_dataset)
	tpd(i) = mean(tags_per_dataset{i});
	
end

h=figure(2);
hist(tpd,0:1:19)
axis([-1 19 0 18])
xlabel('Average tags per Dataset')
ylabel('Number of ODPs')

W = 4; H = 3;
set(h,'PaperUnits','inches')
set(h,'PaperOrientation','portrait');
set(h,'PaperSize',[H,W])
set(h,'PaperPosition',[0,0,W,H])

FN = findall(h,'-property','FontName');
set(FN,'FontName','/usr/share/fonts/dejavu/DejaVuSerifCondensed.ttf');
FS = findall(h,'-property','FontSize');
set(FS,'FontSize',8);

print(h,'-dpng','-color','~/ownCloud/Documents Cloud/Bonn/EIS/Papers/2016/ICSC_Semantic_Tagging/images/tags_per_dataset.png')

##################

similarity;

h=figure(3);
hist(similarity(:,2),0:0.01:0.3)
set(gca,'XTick',[0:0.025:0.3])
set(gca,'XTickLabel',[0:2.5:30])
axis([-.01 .3 0 25])

xlabel('% of very similar pair of tags in relation to the total number of tags')
ylabel('Number of ODPs')

W = 4; H = 3;
set(h,'PaperUnits','inches')
set(h,'PaperOrientation','portrait');
set(h,'PaperSize',[H,W])
set(h,'PaperPosition',[0,0,W,H])

FN = findall(h,'-property','FontName');
set(FN,'FontName','/usr/share/fonts/dejavu/DejaVuSerifCondensed.ttf');
FS = findall(h,'-property','FontSize');
set(FS,'FontSize',8);

print(h,'-dpng','-color','~/ownCloud/Documents Cloud/Bonn/EIS/Papers/2016/ICSC_Semantic_Tagging/images/similarity.png')
