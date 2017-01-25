# home-assistant-example
home-assistant real configuration


## camera motion trigger

![Alt text](https://g.gravizo.com/g?
digraph G {
    size ="5,5";
    
    camera -> ftp [label="on motion"]
    ftp -> incron -> onmotion
    ftp [label="ftp server"]
    onmotion [label="on-motion.sh"]
    onmotion -> hass [label="REST API"]
    onmotion -> image [style="box"]
    image [shape=box,style=filled,color=".7 .3 1.0"]
    hass -> telegram
    image -> telegram -> user
    user [shape=box,style=filled,color=".4 .5 1.0"]
}
)
