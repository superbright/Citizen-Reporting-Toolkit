      //**********************************************************************************
      //********  LEAFLET HEXBIN LAYER CLASS *********************************************
      //**********************************************************************************
      L.HexbinLayer = L.Class.extend({
        includes: L.Mixin.Events,
        initialize: function (rawData, options) {
          this.levels = {};
          this.layout = d3.hexbin().radius(10);
          this.rscale = d3.scale.sqrt().range([0, 10]).clamp(true);
          this.rwData = rawData;
          this.config = options;
        },
        project: function(x) {
          var point = this.map.latLngToLayerPoint([x[1], x[0]]);
          return [point.x, point.y];
        },
        getBounds: function(d) {
          var b = d3.geo.bounds(d)
          return L.bounds(this.project([b[0][0], b[1][1]]), this.project([b[1][0], b[0][1]]));
        },
        update: function () {
          var pad = 100, xy = this.getBounds(this.rwData), zoom = this.map.getZoom();

          this.container
            .attr("width", xy.getSize().x + (2 * pad))
            .attr("height", xy.getSize().y + (2 * pad))
            .style("margin-left", (xy.min.x - pad) + "px")
            .style("margin-top", (xy.min.y - pad) + "px");

          if (!(zoom in this.levels)) {
              this.levels[zoom] = this.container.append("g").attr("class", "zoom-" + zoom);
              this.genHexagons(this.levels[zoom]);
              this.levels[zoom].attr("transform", "translate(" + -(xy.min.x - pad) + "," + -(xy.min.y - pad) + ")");
          }
          if (this.curLevel) {
            this.curLevel.style("display", "none");
          }
          this.curLevel = this.levels[zoom];
          this.curLevel.style("display", "inline");
        },
        genHexagons: function (container) {
          var data = this.rwData.features.map(function (d) {
            var coords = this.project(d.geometry.coordinates)
            return [coords[0],coords[1], d.properties];
          }, this);

          var bins = this.layout(data);
          var hexagons = container.selectAll(".hexagon").data(bins);

          var counts = [];
          bins.map(function (elem) { counts.push(elem.length) });
          this.rscale.domain([0, (ss.mean(counts) + (ss.standard_deviation(counts) * 3))]);

          var path = hexagons.enter().append("path").attr("class", "hexagon");
          this.config.style.call(this, path);

          that = this;
          hexagons
            .attr("d", function(d) { return that.layout.hexagon(that.rscale(d.length)); })
            .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
            .on("mouseover", function (d) { 
              var s=0, k=0;
              d.map(function(e){
                if (e.length === 3) e[2].group === 1 ? ++k : ++s;
              });
              that.config.mouse.call(this, [s,k]);
              d3.select("#tooltip")
                .style("visibility", "visible")
                .style("top", function () { return (d3.event.pageY - 130)+"px"})
                .style("left", function () { return (d3.event.pageX - 130)+"px";})
            })
            .on("mouseout", function (d) { d3.select("#tooltip").style("visibility", "hidden") });
        },
        addTo: function (map) {
          map.addLayer(this);
          return this;
        },
        onAdd: function (map) {
          this.map = map;
          var overlayPane = this.map.getPanes().overlayPane;

          if (!this.container || overlayPane.empty) {
              this.container = d3.select(overlayPane)
                  .append('svg')
                      .attr("id", "hex-svg")
                      .attr('class', 'leaflet-layer leaflet-zoom-hide');
          }
          map.on({ 'moveend': this.update }, this);
          this.update();
        }
      });

      L.hexbinLayer = function (data, styleFunction) {
        return new L.HexbinLayer(data, styleFunction);
      };