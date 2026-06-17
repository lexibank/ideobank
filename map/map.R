# R version 4.3.1 (2023-06-16) -- "Beagle Scouts"
library(readr) # v2.1.4
library(dplyr) # v1.1.3
library(ggplot2) # v3.4.3
library(ggrepel) # v0.9.3
library(rnaturalearth) # v0.3.2
library(rnaturalearthdata) # v0.1.0
library(viridisLite) # v0.4.2
library(viridis) # v0.6.3

# Loading the data
languages <- read_csv('../cldf/languages.csv')

# Downloading the map
spdf_sa <- ne_countries(continent=c("south america"),
                        scale="medium", 
                        returnclass="sf")

rivers <- ne_download(scale = 50, type = 'rivers_lake_centerlines', category = 'physical', returnclass = "sf")

colors <- c('#416dff', '#ca2800', '#ff28ba', '#1c007d', '#aeff0c', '#1c5951', '#49caff', '#35926d',
            '#590000', '#65008e', '#ae0069', '#f7b69a', '#ba10c2', '#510039', '#00650c', '#0096a6',
            '#20aa00', '#ffaeeb', '#ff316d', '#0431ff', '#31e7ce')

# Plotting the language points and labels on the map
map_lex <- ggplot(data=languages) +
  geom_sf(data = spdf_sa) +
  geom_sf(data = rivers) +
  coord_sf(ylim=c(-25, 12), xlim= c(-85, -30)) +
  geom_point(aes(x=Longitude,y=Latitude, fill=Family), size=6, shape=21) +
  scale_fill_manual(values = colors, name='Language family') +
  labs(caption = "Data: Glottolog") +
  theme_bw() +
  guides(fill=guide_legend(ncol=1)) +
  theme(legend.position="right",
        axis.title = element_text(size = rel(1)),
        axis.text = element_text(size = rel(1)),
        legend.text = element_text(size = rel(1)),
        legend.title = element_text(size = rel(1.2)))

map_lex
ggsave('fig_map.pdf', map_lex, width=10, height=6, dpi=500)
