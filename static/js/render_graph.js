var colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"];

var legend = d3.select('#legend');

var graph_outer = d3.select('#graph'),
  width = 1000,
  height = 1000;
  graph_outer.attr("viewBox", [0, 0, width, height]);
  graph_inner = graph_outer.append("g");
d3.csv('/node.csv', function (d) {
  d.id = +d.id;
  d.name = d.id;
  d.color = +d.new;
  d.number = +d.number;
  d.size = "Size: " + d.number + "\n";
  if(d.old_number != "Nan") {
    d.size += "Old size: " + d.old_number + "\n";
  }
  return d;
}).then(function (dnodes) {
  var dlinks = []
  d3.csv('/edge.csv', function (d) {
    if (d.id1 !== d.id2) {
      dlinks.push({
        source: +d.id1,
        target: +d.id2,
        tag: d.types,
      });
    }
  }).then(function () {
    var link = graph_inner
      .selectAll('.edge')
      .data(dlinks)
      .enter()
      .append('polyline')
      .attr('class', 'edge')
      .attr('marker-mid', 'url(#arrowhead)')
      .style('stroke', function (d) {
        return 'grey';
      });

    var node = graph_inner
      .selectAll('.node')
      .data(dnodes)
      .enter()
      .append('g')
      .attr('class', 'node');

    node
      .append('circle')
      .attr('r', function(d) { return 4*Math.log(d.number + 1) } )
      .style('fill', function (d) {
        return colors[d.color];
      });

    node
      .append('circle')
      .attr('r', function(d) { return 2*Math.log(d.number + 1) } )
      .style('fill', function (d) {
        if (d.color == 1) {
          return colors[0];
        } else {
          return "none";
        }
      });

    node.append('title').text(function (d) {
      return d.labels + "\n" + d.size + "Properties:\n" + d.properties.replaceAll(":", "\n");
    });

    node
      .append('text')
      .attr('dx', function (d) {return 4*Math.log(d.number + 1);})
      .attr('dy', function (d) {return 4*Math.log(d.number + 1);})
      .text(function (d) {
        if (d.labels.length > 25) {
          return d.labels.slice(0, 25) + '...';
        }
        return d.labels;
      });

      var link_text = graph_inner
      .selectAll('.edge_text')
      .data(dlinks)
      .enter()
      .append('text')
      .attr('dx', 10)
      .attr('dy', 10)
      .text(function (d) {
        return d.tag;
      });
    d3
      .forceSimulation(dnodes)
      .force(
        'link',
        d3
          .forceLink()
          .id(function (d) {
            return d.id;
          })
          .distance(700)
          .strength(1)
          .links(dlinks)
      )
      .force('charge', d3.forceManyBody().strength(-10000))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .on('tick', update);

    var dragHandler = d3.drag()
      .on("drag", function (event, d) {
          d.x = event.x;
          d.y = event.y;
          update();
      });

  dragHandler(graph_outer.selectAll(".node"));
  var zoom = d3.zoom().extent([[0, 0], [width, height]]).scaleExtent([0.1, 10]).on("zoom", zoomed);
  graph_outer
    .call(zoom)
    .call(zoom.scaleBy, 0.25);
  function zoomed({transform}) {
    graph_inner.attr("transform", transform);
  }
    function update() {
      link
      .attr("points", function(d) {
        return [
             d.source.x, d.source.y,
             (d.source.x + 3 * d.target.x) / 4,
             (d.source.y + 3 * d.target.y) / 4,
             d.target.x, d.target.y
        ].join(',');
      });
      link_text.attr('transform', function (d) {
        return (
          'translate(' +
          (d.source.x + 3 * d.target.x) / 4 +
          ', ' +
          (d.source.y + 3 * d.target.y) / 4 +
          ')'
        );
      });
      node.attr('transform', function (d) {
        return 'translate(' + d.x + ', ' + d.y + ')';
      });
    }
  });
});