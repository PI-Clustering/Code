var colors = d3.scaleOrdinal(d3.schemeCategory10);

var svg = d3.select('#graph'),
  width = svg.node().getBoundingClientRect().width,
  height = svg.node().getBoundingClientRect().height;
  svg.attr("viewBox", [0, 0, width, height]);
  g = svg.append("g");
d3.csv('/node.csv', function (d) {
  d.id = +d.id;
  d.name = d.id;
  d.color = +d.id;
  d.number = +d.number;
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
    var link = g
      .selectAll('.edge')
      .data(dlinks)
      .enter()
      .append('line')
      .attr('class', 'edge')
      .attr('marker-end', 'url(#arrowhead)')
      .style('stroke', function (d) {
        return 'green';
      });

    var link_text = g
      .selectAll('.edge_text')
      .data(dlinks)
      .enter()
      .append('text')
      .attr('style', 'font-size : x-small')
      .text(function (d) {
        return d.tag;
      });


    var node = g
      .selectAll('.node')
      .data(dnodes)
      .enter()
      .append('g')
      .attr('class', 'node');

    node
      .append('circle')
      .attr('r', function(d){ return 4*Math.log(d.number)} )
      .style('fill', function (d, i) {
        return colors(d.color);
      });

    node.append('title').text(function (d) {
      return d.properties;
    });

    node
      .append('text')
      .attr('dx', 15)
      .attr('dy', 20)
      .text(function (d) {
        return d.labels;
      });

    node
      .append('text')
      .attr('dx', 15)
      .attr('dy', 40)
      .attr('style', 'font-size : x-small')
      .text(function (d) {
        if (d.properties.length > 25) {
          return d.properties.slice(0, 25) + '...';
        }
        return d.properties;
      });
    console.log(dnodes);
    console.log(dlinks);
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
      .force('charge', d3.forceManyBody().strength(0))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .on('tick', update);

    var dragHandler = d3.drag()
      .on("drag", function (event, d) {
          d.x = event.x;
          d.y = event.y;
          update();
      });

  dragHandler(svg.selectAll(".node"));
  svg.call(d3.zoom().extent([[0, 0], [width, height]]).scaleExtent([0.1, 10]).on("zoom", zoomed));
  function zoomed({transform}) {
    g.attr("transform", transform);
  }
    function update() {
      link
        .attr('x1', function (d) {
          return d.source.x;
        })
        .attr('y1', function (d) {
          return d.source.y;
        })
        .attr('x2', function (d) {
          return d.target.x;
        })
        .attr('y2', function (d) {
          return d.target.y;
        });
      link_text.attr('transform', function (d) {
        return (
          'translate(' +
          (d.source.x + d.target.x) / 2 +
          ', ' +
          (d.source.y + d.target.y) / 2 +
          ')'
        );
      });
      node.attr('transform', function (d) {
        return 'translate(' + d.x + ', ' + d.y + ')';
      });
    }
  });
});
