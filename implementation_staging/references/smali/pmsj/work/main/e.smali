.class public final Lpmsj/work/main/e;
.super Ljava/lang/Object;


# static fields
.field public static a:Lpmsj/work/main/i;

.field static b:[B

.field static c:S

.field public static d:I

.field private static e:Lpmsj/work/main/c;

.field private static f:Ljava/lang/String;


# direct methods
.method static constructor <clinit>()V
    .locals 1

    invoke-static {}, Lpmsj/work/main/c;->a()Lpmsj/work/main/c;

    move-result-object v0

    sput-object v0, Lpmsj/work/main/e;->e:Lpmsj/work/main/c;

    const/4 v0, 0x0

    sput v0, Lpmsj/work/main/e;->d:I

    return-void
.end method

.method public constructor <init>(Lpmsj/work/main/i;)V
    .locals 0

    invoke-direct {p0}, Ljava/lang/Object;-><init>()V

    sput-object p1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    return-void
.end method

.method private static A(Lpmsj/work/main/w;)V
    .locals 6

    const/4 v5, 0x2

    const/4 v4, 0x0

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    return-void

    :pswitch_0
    new-array v1, v5, [La/c/i;

    move v2, v4

    :goto_1
    if-ge v2, v5, :cond_1

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int/lit8 v3, v2, 0x1

    invoke-virtual {v0, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    aput-object v0, v1, v2

    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_1

    :cond_1
    aget-object v0, v1, v4

    invoke-virtual {v0}, La/c/i;->b()I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/f;->d(I)B

    move-result v0

    const/4 v2, -0x1

    if-eq v2, v0, :cond_2

    sget-object v2, Lpmsj/work/b/f;->q:Ljava/util/Vector;

    invoke-virtual {v2, v0}, Ljava/util/Vector;->removeElementAt(I)V

    :cond_2
    sget-object v0, Lpmsj/work/b/f;->q:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0xcb

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/du;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x25c

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ez;

    if-eqz p0, :cond_3

    invoke-virtual {p0}, Lpmsj/work/e/du;->i()V

    :cond_3
    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/e/ez;->i()V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
    .end packed-switch
.end method

.method private static B(Lpmsj/work/main/w;)V
    .locals 8

    const/4 v3, 0x2

    const/16 v7, 0x14b

    const/4 v6, 0x1

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    return-void

    :pswitch_0
    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    if-lez v0, :cond_0

    sget-object v1, Lpmsj/work/b/f;->o:Lpmsj/work/b/y;

    if-nez v1, :cond_1

    new-instance v1, Lpmsj/work/b/y;

    invoke-direct {v1}, Lpmsj/work/b/y;-><init>()V

    sput-object v1, Lpmsj/work/b/f;->o:Lpmsj/work/b/y;

    :cond_1
    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    sub-int/2addr v1, v3

    div-int/2addr v1, v0

    :goto_1
    if-ge v2, v0, :cond_2

    mul-int v3, v2, v1

    add-int/lit8 v3, v3, 0x2

    invoke-static {v1, v3, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v3

    new-instance v4, Lpmsj/work/b/z;

    aget-object v5, v3, v6

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v5

    invoke-direct {v4, v5, v3}, Lpmsj/work/b/z;-><init>(I[La/c/i;)V

    sget-object v5, Lpmsj/work/b/f;->o:Lpmsj/work/b/y;

    aget-object v3, v3, v6

    invoke-virtual {v3}, La/c/i;->b()I

    move-result v3

    invoke-virtual {v5, v3, v4}, Lpmsj/work/b/y;->a(ILpmsj/work/b/w;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_1

    :cond_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v7}, Lpmsj/work/d/n;->h(I)V

    goto :goto_0

    :pswitch_1
    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x9

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(I)Z

    sget-object v0, Lpmsj/work/b/f;->o:Lpmsj/work/b/y;

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/y;->b(I)Lpmsj/work/b/w;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/z;

    if-eqz v0, :cond_0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v0, Lpmsj/work/b/z;->B:I

    const/4 v1, 0x3

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/String;->toString()Ljava/lang/String;

    move-result-object v1

    iput-object v1, v0, Lpmsj/work/b/z;->A:Ljava/lang/String;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v7}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/dl;

    if-eqz p0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {p0}, Lpmsj/work/e/dl;->i()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->b(Ljava/lang/String;)V

    goto/16 :goto_0

    :pswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v7, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
    .end packed-switch
.end method

.method private static C(Lpmsj/work/main/w;)V
    .locals 5

    const/4 v3, 0x1

    const/4 v2, 0x0

    const-string v4, "KEY_NOTICE"

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    const/4 v1, 0x2

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v1

    sput-object v1, Lpmsj/work/a/c;->d:Ljava/lang/String;

    :try_start_0
    const-string v1, "KEY_NOTICE"

    invoke-static {v1}, La/c/s;->a(Ljava/lang/String;)Ljava/lang/String;

    move-result-object v1

    if-eqz v1, :cond_1

    invoke-static {v1}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    move-result v1

    :goto_0
    if-le v0, v1, :cond_0

    invoke-static {}, Lpmsj/work/main/w;->a()Lpmsj/work/main/w;

    const/16 v1, 0x5fd

    invoke-static {v1, v2, v3}, Lpmsj/work/main/w;->a(IBI)V

    const-string v1, "KEY_NOTICE"

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, ""

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-static {v4, v0}, La/c/s;->a(Ljava/lang/String;Ljava/lang/String;)V

    :cond_0
    return-void

    :catch_0
    move-exception v1

    move v1, v2

    goto :goto_0

    :cond_1
    move v1, v2

    goto :goto_0
.end method

.method private static D(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x147

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x148

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_1
        :pswitch_1
        :pswitch_1
    .end packed-switch
.end method

.method private static E(Lpmsj/work/main/w;)V
    .locals 9

    const/4 v8, 0x3

    const/16 v7, 0xcb

    const/4 v5, 0x2

    const/4 v4, 0x0

    const/4 v6, 0x1

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    const/4 v1, 0x0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    return-void

    :pswitch_0
    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    if-lez v0, :cond_0

    sget-object v1, Lpmsj/work/b/f;->n:Lpmsj/work/b/y;

    if-nez v1, :cond_1

    new-instance v1, Lpmsj/work/b/y;

    invoke-direct {v1}, Lpmsj/work/b/y;-><init>()V

    sput-object v1, Lpmsj/work/b/f;->n:Lpmsj/work/b/y;

    :cond_1
    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    sub-int/2addr v1, v5

    div-int/2addr v1, v0

    move v2, v4

    :goto_1
    if-ge v2, v0, :cond_2

    mul-int v3, v2, v1

    add-int/lit8 v3, v3, 0x2

    invoke-static {v1, v3, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v3

    new-instance v4, Lpmsj/work/b/x;

    aget-object v5, v3, v6

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v5

    invoke-direct {v4, v5, v3}, Lpmsj/work/b/x;-><init>(I[La/c/i;)V

    sget-object v5, Lpmsj/work/b/f;->n:Lpmsj/work/b/y;

    aget-object v3, v3, v6

    invoke-virtual {v3}, La/c/i;->b()I

    move-result v3

    invoke-virtual {v5, v3, v4}, Lpmsj/work/b/y;->a(ILpmsj/work/b/w;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_1

    :cond_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v7}, Lpmsj/work/d/n;->h(I)V

    goto :goto_0

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x145

    invoke-virtual {v0, v1, p0, v6}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x146

    invoke-virtual {v0, v1, p0, v6}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_3
    sget-object v0, Lpmsj/work/b/f;->n:Lpmsj/work/b/y;

    if-eqz v0, :cond_0

    sget-object v0, Lpmsj/work/b/f;->n:Lpmsj/work/b/y;

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    invoke-virtual {p0, v8}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/b/y;->c(IILjava/lang/String;)Lpmsj/work/b/x;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v7}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/du;

    if-eqz p0, :cond_3

    invoke-virtual {p0, v0}, Lpmsj/work/e/du;->a(Lpmsj/work/b/w;)V

    :cond_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x25b

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ax;

    if-eqz p0, :cond_0

    invoke-virtual {p0, v0}, Lpmsj/work/e/ax;->a(Lpmsj/work/b/w;)V

    goto/16 :goto_0

    :pswitch_4
    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    if-lez v0, :cond_0

    iget-object v2, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    sub-int/2addr v2, v5

    div-int/2addr v2, v0

    move-object v3, v1

    move v1, v4

    :goto_2
    if-ge v1, v0, :cond_5

    mul-int v3, v1, v2

    add-int/lit8 v3, v3, 0x2

    invoke-static {v2, v3, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v3

    sget-object v4, Lpmsj/work/b/f;->n:Lpmsj/work/b/y;

    if-eqz v4, :cond_4

    sget-object v4, Lpmsj/work/b/f;->n:Lpmsj/work/b/y;

    invoke-virtual {v4, v3}, Lpmsj/work/b/y;->a([La/c/i;)V

    :cond_4
    add-int/lit8 v1, v1, 0x1

    goto :goto_2

    :cond_5
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v7}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x149

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/az;

    if-eqz p0, :cond_6

    invoke-virtual {p0, v3}, Lpmsj/work/e/az;->a([La/c/i;)V

    :cond_6
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x148

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/dc;

    if-eqz p0, :cond_7

    if-eqz v3, :cond_7

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    const/4 v1, 0x6

    aget-object v1, v3, v1

    invoke-virtual {v1}, La/c/i;->b()I

    move-result v1

    and-int/lit8 v1, v1, 0x1

    if-eqz v1, :cond_8

    const-string v1, "\u719f\u7ec3\u5ea6\uff1a"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/4 v1, 0x4

    aget-object v1, v3, v1

    invoke-virtual {v1}, La/c/i;->b()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    const-string v1, "/"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/4 v1, 0x5

    aget-object v1, v3, v1

    invoke-virtual {v1}, La/c/i;->b()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    :goto_3
    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p0, v0}, Lpmsj/work/e/dc;->d(Ljava/lang/String;)V

    :cond_7
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x25b

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ax;

    if-eqz p0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/ax;->i()V

    goto/16 :goto_0

    :cond_8
    const-string v1, "*9\u6280\u80fd"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v1, "\uff1a"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    aget-object v1, v3, v5

    invoke-virtual {v1}, La/c/i;->b()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    const-string v1, "/"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    aget-object v1, v3, v8

    invoke-virtual {v1}, La/c/i;->b()I

    move-result v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    const/16 v1, 0x20

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    const-string v1, "\u7ea7"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_3

    :pswitch_5
    new-array v1, v5, [La/c/i;

    move v2, v4

    :goto_4
    if-ge v2, v5, :cond_9

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int/lit8 v3, v2, 0x1

    invoke-virtual {v0, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    aput-object v0, v1, v2

    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_4

    :cond_9
    aget-object v0, v1, v4

    invoke-virtual {v0}, La/c/i;->b()I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/f;->c(I)B

    move-result v0

    const/4 v2, -0x1

    if-eq v2, v0, :cond_a

    sget-object v2, Lpmsj/work/b/f;->p:Ljava/util/Vector;

    invoke-virtual {v2, v0}, Ljava/util/Vector;->removeElementAt(I)V

    :cond_a
    sget-object v0, Lpmsj/work/b/f;->p:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x146

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x148

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :pswitch_6
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x149

    invoke-virtual {v0, v1, p0, v4}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_4
        :pswitch_5
        :pswitch_6
    .end packed-switch
.end method

.method private static F(Lpmsj/work/main/w;)V
    .locals 3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x142

    const/4 v2, 0x0

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    return-void
.end method

.method private static G(Lpmsj/work/main/w;)V
    .locals 3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x3d

    const/4 v2, 0x0

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    return-void
.end method

.method private static H(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x191

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    return-void
.end method

.method private static I(Lpmsj/work/main/w;)V
    .locals 9

    const/4 v3, 0x2

    const/4 v8, 0x0

    invoke-virtual {p0, v8}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    const/4 v1, 0x1

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    if-gtz v1, :cond_0

    :goto_0
    return-void

    :cond_0
    iget-object v2, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    sub-int/2addr v2, v3

    div-int/2addr v2, v1

    packed-switch v0, :pswitch_data_0

    :cond_1
    :goto_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x141

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/dk;

    if-eqz p0, :cond_2

    invoke-virtual {p0}, Lpmsj/work/e/dk;->ag()V

    :cond_2
    invoke-static {v8, v8}, Lpmsj/work/main/t;->a(ZZ)V

    goto :goto_0

    :pswitch_0
    move v3, v8

    :goto_2
    if-ge v3, v1, :cond_1

    add-int/lit8 v0, v2, 0x1

    new-array v4, v0, [La/c/i;

    move v5, v8

    :goto_3
    if-ge v5, v2, :cond_3

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int/lit8 v6, v5, 0x2

    mul-int v7, v3, v2

    add-int/2addr v6, v7

    invoke-virtual {v0, v6}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    aput-object v0, v4, v5

    add-int/lit8 v0, v5, 0x1

    move v5, v0

    goto :goto_3

    :cond_3
    new-instance v0, La/c/n;

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    invoke-direct {v0, v5, v6}, La/c/n;-><init>(J)V

    aput-object v0, v4, v2

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/b/ab;->K:Ljava/util/Vector;

    invoke-virtual {v0, v4}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_2

    :pswitch_1
    add-int/lit8 v0, v2, 0x1

    new-array v1, v0, [La/c/i;

    move v3, v8

    :goto_4
    if-ge v3, v2, :cond_4

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int/lit8 v4, v3, 0x2

    invoke-virtual {v0, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    aput-object v0, v1, v3

    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_4

    :cond_4
    new-instance v0, La/c/n;

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v3

    invoke-direct {v0, v3, v4}, La/c/n;-><init>(J)V

    aput-object v0, v1, v2

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    sget-byte v2, Lpmsj/work/b/ab;->M:B

    aget-object v2, v1, v2

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v0, v2}, Lpmsj/work/b/ab;->b(I)Z

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/b/ab;->K:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_1

    :pswitch_2
    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/b/ab;->b(I)Z

    goto/16 :goto_1

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
        :pswitch_1
        :pswitch_2
    .end packed-switch
.end method

.method private static J(Lpmsj/work/main/w;)V
    .locals 4

    const/4 v2, 0x0

    const-string v3, ""

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "http://"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v1, v1, Lpmsj/work/main/i;->f:La/c/t;

    invoke-virtual {v1}, La/c/t;->b()V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v1, v1, Lpmsj/work/main/i;->f:La/c/t;

    invoke-virtual {v1}, La/c/t;->c()V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v1, v1, Lpmsj/work/main/i;->f:La/c/t;

    iput-byte v2, v1, La/c/t;->b:B

    const-string v1, ""

    const-string v1, ""

    invoke-static {v0, v3, v3}, Lpmsj/work/main/c;->a(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    return-void
.end method

.method private static K(Lpmsj/work/main/w;)V
    .locals 15

    const/16 v14, 0xe

    const/4 v13, 0x3

    const/4 v12, 0x4

    const/4 v11, 0x1

    const/4 v3, 0x0

    invoke-static {v3, v3}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    if-nez v1, :cond_7

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v1, v1, Lpmsj/work/main/i;->h:La/c/q;

    invoke-virtual {v1}, La/c/q;->h()Z

    move-result v1

    if-nez v1, :cond_0

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v1, v1, Lpmsj/work/main/i;->h:La/c/q;

    sget v2, Lpmsj/work/main/i;->g:I

    invoke-virtual {v1, v2}, La/c/q;->e(I)V

    :cond_0
    invoke-static {}, Lpmsj/work/main/f;->b()V

    sget v1, Lpmsj/work/main/i;->m:I

    invoke-static {v1}, Lpmsj/work/main/i;->b(I)Z

    move-result v1

    if-eqz v1, :cond_3

    sget-object v1, Lpmsj/work/main/e;->f:Ljava/lang/String;

    if-eqz v1, :cond_3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x162

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/bz;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x136

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v1

    check-cast v1, Lpmsj/work/e/bd;

    if-eqz v1, :cond_1

    invoke-virtual {p0, v1}, Lpmsj/work/e/bz;->a(Lpmsj/work/d/c;)V

    :cond_1
    const/16 v1, 0x438

    invoke-static {v1, v12}, Lpmsj/work/main/w;->a(IS)V

    invoke-static {v11, v3}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x174

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/da;

    sget-object v1, Lpmsj/work/main/e;->f:Ljava/lang/String;

    invoke-virtual {p0, v1}, Lpmsj/work/e/da;->g(Ljava/lang/String;)V

    const/4 v1, 0x0

    sput-object v1, Lpmsj/work/main/e;->f:Ljava/lang/String;

    :cond_2
    :goto_0
    return-void

    :cond_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v14}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v1

    move-object v0, v1

    check-cast v0, Lpmsj/work/e/cv;

    move-object v7, v0

    invoke-virtual {p0, v11}, Lpmsj/work/main/w;->a(I)B

    move-result v8

    if-nez v8, :cond_5

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x162

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    const/16 v1, 0x438

    invoke-static {v1, v12}, Lpmsj/work/main/w;->a(IS)V

    invoke-static {v11, v3}, Lpmsj/work/main/t;->a(ZZ)V

    :cond_4
    :goto_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x136

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0xa

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->a(I)Z

    goto :goto_0

    :cond_5
    if-eqz v7, :cond_4

    move v9, v3

    :goto_2
    if-ge v9, v8, :cond_6

    const/16 v1, 0xf

    mul-int/lit8 v2, v9, 0xf

    add-int/lit8 v2, v2, 0x2

    invoke-static {v1, v2, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v10

    aget-object v1, v10, v13

    invoke-virtual {v1}, La/c/i;->b()I

    move-result v5

    new-instance v1, Lpmsj/work/b/v;

    aget-object v2, v10, v3

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    const v4, 0x186a0

    move v6, v3

    invoke-direct/range {v1 .. v6}, Lpmsj/work/b/v;-><init>(IBIIZ)V

    aget-object v2, v10, v3

    invoke-virtual {v1, v11, v2}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    const/16 v2, 0xb

    aget-object v4, v10, v11

    invoke-virtual {v1, v2, v4}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    const/4 v2, 0x7

    const/4 v4, 0x2

    aget-object v4, v10, v4

    invoke-virtual {v1, v2, v4}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    const/4 v2, 0x6

    aget-object v4, v10, v13

    invoke-virtual {v1, v2, v4}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    const/16 v2, 0xc

    aget-object v4, v10, v12

    invoke-virtual {v4}, La/c/i;->b()I

    move-result v4

    div-int/lit8 v4, v4, 0xa

    invoke-virtual {v1, v2, v4}, Lpmsj/work/b/v;->a(BI)V

    const/16 v2, 0x27

    aget-object v4, v10, v12

    invoke-virtual {v4}, La/c/i;->b()I

    move-result v4

    rem-int/lit8 v4, v4, 0xa

    invoke-virtual {v1, v2, v4}, Lpmsj/work/b/v;->a(BI)V

    const/4 v2, 0x5

    aget-object v2, v10, v2

    invoke-virtual {v1, v13, v2}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    invoke-virtual {v1, v5}, Lpmsj/work/b/v;->M(I)V

    const/4 v2, 0x2

    aget-object v2, v10, v2

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v1, v2}, Lpmsj/work/b/v;->e(I)V

    const/4 v2, 0x7

    aget-object v2, v10, v2

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v1, v2}, Lpmsj/work/b/v;->d(I)V

    const/16 v2, 0x8

    aget-object v2, v10, v2

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v1, v2}, Lpmsj/work/b/v;->z(I)V

    const/16 v2, 0x9

    aget-object v2, v10, v2

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v1, v2}, Lpmsj/work/b/v;->A(I)V

    const/16 v2, 0xa

    aget-object v2, v10, v2

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v1, v2}, Lpmsj/work/b/v;->B(I)V

    const/16 v2, 0xb

    aget-object v2, v10, v2

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v1, v2}, Lpmsj/work/b/v;->C(I)V

    const/16 v2, 0xc

    aget-object v2, v10, v2

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v1, v2}, Lpmsj/work/b/v;->D(I)V

    const/16 v2, 0xd

    aget-object v2, v10, v2

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v1, v2}, Lpmsj/work/b/v;->E(I)V

    aget-object v2, v10, v14

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v1, v2}, Lpmsj/work/b/v;->F(I)V

    const/4 v2, 0x6

    aget-object v2, v10, v2

    invoke-virtual {v2}, La/c/i;->b()I

    move-result v2

    invoke-virtual {v7, v2, v1}, Lpmsj/work/e/cv;->a(ILpmsj/work/b/v;)V

    add-int/lit8 v1, v9, 0x1

    move v9, v1

    goto/16 :goto_2

    :cond_6
    invoke-virtual {v7}, Lpmsj/work/e/cv;->ag()V

    sget v1, Lpmsj/work/main/i;->r:I

    invoke-static {v1}, Lpmsj/work/main/i;->b(I)Z

    move-result v1

    if-eqz v1, :cond_4

    sget v1, Lpmsj/work/main/i;->r:I

    invoke-static {v1}, Lpmsj/work/main/i;->d(I)V

    goto/16 :goto_1

    :cond_7
    if-ne v1, v11, :cond_8

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v14}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v1

    check-cast v1, Lpmsj/work/e/cv;

    if-eqz v1, :cond_2

    invoke-virtual {p0, v11}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    invoke-virtual {v1, v2}, Lpmsj/work/e/cv;->C(I)V

    goto/16 :goto_0

    :cond_8
    if-ne v1, v12, :cond_2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x162

    invoke-virtual {v1, v2, p0, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_0
.end method

.method private static L(Lpmsj/work/main/w;)V
    .locals 6

    const/4 v5, 0x0

    const/4 v4, 0x3

    const/4 v1, 0x1

    const/4 v3, 0x2

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    const-string v0, "ACT_MAP_CLEAR"

    invoke-static {v0}, Lpmsj/work/e/ba;->g(Ljava/lang/String;)V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->a(I)B

    move-result v3

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/b/m;->a(BBB)V

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/main/k;->j()V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->f(I)[B

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/m;->a([B)V

    goto :goto_0

    :pswitch_3
    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->f(I)[B

    move-result-object v2

    invoke-virtual {v1, v2, v0}, Lpmsj/work/b/m;->a([BI)V

    goto :goto_0

    :pswitch_4
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->f(I)[B

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/m;->b([B)V

    goto :goto_0

    :pswitch_5
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->f(I)[B

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/m;->c([B)V

    goto :goto_0

    :pswitch_6
    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->f(I)[B

    move-result-object v3

    invoke-virtual {v2, v0, v1, v3}, Lpmsj/work/b/m;->a(SS[B)V

    goto :goto_0

    :pswitch_7
    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    sget-object v1, Lpmsj/work/b/p;->d:[B

    if-nez v1, :cond_0

    new-array v0, v0, [B

    sput-object v0, Lpmsj/work/b/p;->d:[B

    :cond_0
    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->f(I)[B

    move-result-object v0

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    sget-object v2, Lpmsj/work/b/p;->d:[B

    array-length v3, v0

    invoke-static {v0, v5, v2, v1, v3}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    goto/16 :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_2
        :pswitch_2
        :pswitch_3
        :pswitch_3
        :pswitch_4
        :pswitch_4
        :pswitch_5
        :pswitch_5
        :pswitch_0
        :pswitch_0
        :pswitch_6
        :pswitch_6
        :pswitch_0
        :pswitch_0
        :pswitch_7
    .end packed-switch
.end method

.method private static M(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v0, 0x0

    :goto_0
    const/16 v1, 0x15

    if-ge v0, v1, :cond_1

    const/16 v1, 0xf

    if-ge v0, v1, :cond_0

    sget-object v1, Lpmsj/work/main/c;->a:[I

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    div-int/lit8 v2, v2, 0x64

    aput v2, v1, v0

    :goto_1
    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    :cond_0
    sget-object v1, Lpmsj/work/main/c;->a:[I

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    aput v2, v1, v0

    goto :goto_1

    :cond_1
    return-void
.end method

.method private static N(Lpmsj/work/main/w;)V
    .locals 8

    const/4 v7, 0x0

    const/4 v6, 0x1

    const/4 v5, 0x0

    const-string v0, "processUserInfoCmd"

    invoke-static {v0}, Lpmsj/work/e/ba;->g(Ljava/lang/String;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/d/n;->e()V

    const/16 v0, 0x17

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/v;->H(I)I

    move-result v0

    new-instance v1, Lpmsj/work/b/ab;

    const/4 v2, 0x2

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    const/4 v3, 0x7

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v3

    invoke-direct {v1, v2, v0, v3}, Lpmsj/work/b/ab;-><init>(III)V

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    move v2, v6

    :goto_0
    if-gt v2, v0, :cond_0

    iget-object v3, v1, Lpmsj/work/b/ab;->p:Ljava/util/Vector;

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_0
    const/16 v2, 0x1f

    sub-int/2addr v2, v0

    sub-int/2addr v2, v6

    move v3, v5

    :goto_1
    if-ge v3, v2, :cond_1

    iget-object v4, v1, Lpmsj/work/b/ab;->p:Ljava/util/Vector;

    invoke-virtual {v4, v7}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v3, v3, 0x1

    goto :goto_1

    :cond_1
    iget-object v2, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    sub-int/2addr v2, v6

    :goto_2
    if-ge v0, v2, :cond_2

    iget-object v3, v1, Lpmsj/work/b/ab;->p:Ljava/util/Vector;

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v4

    invoke-virtual {v3, v4}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v0, v0, 0x1

    goto :goto_2

    :cond_2
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    sput v0, Lpmsj/work/main/f;->k:I

    const/16 v0, 0x16

    invoke-virtual {v1, v0}, Lpmsj/work/b/ab;->f(B)I

    move-result v0

    invoke-virtual {v1, v0}, Lpmsj/work/b/ab;->G(I)V

    invoke-virtual {v1}, Lpmsj/work/b/ab;->r()V

    invoke-virtual {v1}, Lpmsj/work/b/ab;->Q()V

    const/16 v0, 0x19

    invoke-virtual {v1, v0}, Lpmsj/work/b/ab;->f(B)I

    move-result v0

    invoke-virtual {v1, v0, v5}, Lpmsj/work/b/ab;->f(II)V

    sput-object v7, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    sput-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    const/16 v0, 0xe

    invoke-static {v0, v5}, Lpmsj/work/main/e;->a(SI)V

    invoke-static {v5, v5}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v2, 0x3d

    invoke-virtual {v0, v2}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    invoke-static {}, Lpmsj/work/main/t;->b()Lpmsj/work/main/t;

    move-result-object v0

    iput-boolean v6, v0, Lpmsj/work/main/t;->m:Z

    invoke-static {}, Lpmsj/work/main/x;->d()V

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/main/k;->o()V

    invoke-virtual {v1}, Lpmsj/work/b/ab;->u()I

    move-result v0

    invoke-static {v0}, Lpmsj/work/main/f;->a(I)V

    invoke-virtual {v1}, Lpmsj/work/b/ab;->u()I

    move-result v0

    invoke-static {v0}, Lpmsj/work/main/f;->d(I)V

    invoke-virtual {v1}, Lpmsj/work/b/ab;->af()Z

    move-result v0

    if-eqz v0, :cond_3

    const v0, 0x9c40

    invoke-virtual {v1, v0, v6}, Lpmsj/work/b/ab;->c(IZ)La/a/d;

    :cond_3
    const/16 v0, 0x463

    new-instance v1, La/c/h;

    invoke-direct {v1, v5}, La/c/h;-><init>(B)V

    new-instance v2, La/c/h;

    const/16 v3, 0x35

    invoke-direct {v2, v3}, La/c/h;-><init>(B)V

    new-instance v3, La/c/o;

    const/16 v4, 0x7d0

    invoke-direct {v3, v4}, La/c/o;-><init>(S)V

    new-instance v4, La/c/o;

    sget-short v5, Lpmsj/work/a/c;->a:S

    invoke-direct {v4, v5}, La/c/o;-><init>(S)V

    invoke-static {v0, v1, v2, v3, v4}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;)V

    return-void
.end method

.method private static O(Lpmsj/work/main/w;)V
    .locals 12

    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/b/m;->o(I)Lpmsj/work/b/v;

    move-result-object v1

    if-nez v1, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    const/4 v2, 0x2

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    const/4 v3, 0x0

    invoke-static {v0}, Lpmsj/work/b/aa;->b(I)[La/c/i;

    move-result-object v4

    const/4 v0, 0x0

    move v5, v3

    move v3, v0

    :goto_1
    if-ge v3, v2, :cond_10

    mul-int/lit8 v0, v3, 0x2

    add-int/lit8 v0, v0, 0x3

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B

    move-result v6

    mul-int/lit8 v0, v3, 0x2

    add-int/lit8 v0, v0, 0x4

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v7

    sparse-switch v6, :sswitch_data_0

    :cond_2
    :goto_2
    const/16 v0, 0x55

    if-eq v6, v0, :cond_3

    const/16 v0, 0x56

    if-ne v6, v0, :cond_b

    :cond_3
    const/16 v0, 0x36

    sub-int v0, v6, v0

    int-to-byte v0, v0

    invoke-virtual {v1, v0}, Lpmsj/work/b/v;->f(B)I

    move-result v0

    int-to-long v8, v0

    invoke-virtual {v7}, La/c/i;->b()I

    move-result v0

    int-to-long v10, v0

    const/16 v0, 0x20

    shl-long/2addr v10, v0

    or-long/2addr v8, v10

    const-wide/16 v10, 0x0

    cmp-long v0, v8, v10

    if-gez v0, :cond_4

    const-wide v10, 0x100000000L

    add-long/2addr v8, v10

    :cond_4
    new-instance v0, La/c/n;

    invoke-direct {v0, v8, v9}, La/c/n;-><init>(J)V

    const/16 v8, 0x36

    sub-int v8, v6, v8

    int-to-byte v8, v8

    invoke-virtual {v1, v8, v0}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    :goto_3
    invoke-virtual {v7}, La/c/i;->b()I

    move-result v7

    sparse-switch v6, :sswitch_data_1

    :cond_5
    :goto_4
    const/16 v0, 0xb

    if-ne v6, v0, :cond_c

    if-eqz v4, :cond_c

    const/4 v0, 0x1

    const/4 v5, 0x5

    aget-object v5, v4, v5

    invoke-virtual {v5, v7}, La/c/i;->a(I)V

    :goto_5
    add-int/lit8 v3, v3, 0x1

    move v5, v0

    goto :goto_1

    :sswitch_0
    invoke-virtual {v7}, La/c/i;->b()I

    move-result v0

    const/high16 v8, 0x2000000

    invoke-virtual {v1, v0, v8}, Lpmsj/work/b/v;->d(II)Z

    move-result v0

    if-eqz v0, :cond_8

    const v0, 0x2143a0

    const/4 v8, 0x1

    invoke-virtual {v1, v0, v8}, Lpmsj/work/b/v;->b(IZ)La/a/d;

    :cond_6
    :goto_6
    invoke-virtual {v7}, La/c/i;->b()I

    move-result v0

    const/high16 v8, 0x20000

    invoke-virtual {v1, v0, v8}, Lpmsj/work/b/v;->d(II)Z

    move-result v0

    if-eqz v0, :cond_9

    const v0, 0x208050

    const/4 v8, 0x1

    invoke-virtual {v1, v0, v8}, Lpmsj/work/b/v;->b(IZ)La/a/d;

    :cond_7
    :goto_7
    invoke-virtual {v7}, La/c/i;->b()I

    move-result v0

    const/high16 v8, 0x1000000

    invoke-virtual {v1, v0, v8}, Lpmsj/work/b/v;->d(II)Z

    move-result v0

    if-eqz v0, :cond_a

    const v0, 0x21b8d0

    const/4 v8, 0x1

    invoke-virtual {v1, v0, v8}, Lpmsj/work/b/v;->b(IZ)La/a/d;

    goto/16 :goto_2

    :cond_8
    invoke-virtual {v7}, La/c/i;->b()I

    move-result v0

    const/high16 v8, 0x2000000

    invoke-virtual {v1, v0, v8}, Lpmsj/work/b/v;->e(II)Z

    move-result v0

    if-eqz v0, :cond_6

    const v0, 0x2143a0

    invoke-virtual {v1, v0}, Lpmsj/work/b/v;->t(I)V

    goto :goto_6

    :cond_9
    invoke-virtual {v7}, La/c/i;->b()I

    move-result v0

    const/high16 v8, 0x20000

    invoke-virtual {v1, v0, v8}, Lpmsj/work/b/v;->e(II)Z

    move-result v0

    if-eqz v0, :cond_7

    const v0, 0x208050

    invoke-virtual {v1, v0}, Lpmsj/work/b/v;->t(I)V

    goto :goto_7

    :cond_a
    invoke-virtual {v7}, La/c/i;->b()I

    move-result v0

    const/high16 v8, 0x1000000

    invoke-virtual {v1, v0, v8}, Lpmsj/work/b/v;->e(II)Z

    move-result v0

    if-eqz v0, :cond_2

    const v0, 0x21b8d0

    invoke-virtual {v1, v0}, Lpmsj/work/b/v;->t(I)V

    goto/16 :goto_2

    :sswitch_1
    invoke-virtual {v7}, La/c/i;->b()I

    move-result v0

    const/16 v8, 0x19

    invoke-virtual {v1, v8}, Lpmsj/work/b/v;->f(B)I

    move-result v8

    invoke-virtual {v1, v0, v8}, Lpmsj/work/b/v;->g(II)V

    goto/16 :goto_2

    :sswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v8, 0x3

    invoke-virtual {v0, v8}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/main/k;

    if-eqz v0, :cond_2

    invoke-virtual {v7}, La/c/i;->b()I

    move-result v8

    invoke-virtual {v0, v8}, Lpmsj/work/main/k;->b_(I)V

    goto/16 :goto_2

    :cond_b
    invoke-virtual {v1, v6, v7}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    goto/16 :goto_3

    :sswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v8, 0x5

    invoke-virtual {v0, v8}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/at;

    if-eqz v0, :cond_5

    invoke-virtual {v0}, Lpmsj/work/e/at;->ap()V

    goto/16 :goto_4

    :sswitch_4
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v8, 0x5

    invoke-virtual {v0, v8}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/at;

    if-eqz v0, :cond_5

    invoke-virtual {v0}, Lpmsj/work/e/at;->ar()V

    goto/16 :goto_4

    :sswitch_5
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->d(I)V

    goto/16 :goto_4

    :sswitch_6
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->y(I)V

    goto/16 :goto_4

    :sswitch_7
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->z(I)V

    goto/16 :goto_4

    :sswitch_8
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->A(I)V

    goto/16 :goto_4

    :sswitch_9
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->B(I)V

    goto/16 :goto_4

    :sswitch_a
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->C(I)V

    goto/16 :goto_4

    :sswitch_b
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->D(I)V

    goto/16 :goto_4

    :sswitch_c
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->E(I)V

    goto/16 :goto_4

    :sswitch_d
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->F(I)V

    goto/16 :goto_4

    :sswitch_e
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->e(I)V

    goto/16 :goto_4

    :sswitch_f
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->I(I)V

    goto/16 :goto_4

    :sswitch_10
    invoke-virtual {v1, v7}, Lpmsj/work/b/v;->J(I)V

    goto/16 :goto_4

    :sswitch_11
    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    if-ne v1, v0, :cond_5

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/4 v0, 0x4

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_4

    :sswitch_12
    invoke-virtual {v1}, Lpmsj/work/b/v;->Q()V

    goto/16 :goto_4

    :cond_c
    const/16 v0, 0x28

    if-ne v6, v0, :cond_d

    if-eqz v4, :cond_d

    const/4 v0, 0x1

    const/4 v5, 0x3

    aget-object v5, v4, v5

    invoke-virtual {v5, v7}, La/c/i;->a(I)V

    goto/16 :goto_5

    :cond_d
    const/16 v0, 0x29

    if-ne v6, v0, :cond_e

    if-eqz v4, :cond_e

    const/4 v0, 0x1

    const/4 v5, 0x2

    aget-object v5, v4, v5

    invoke-virtual {v5, v7}, La/c/i;->a(I)V

    goto/16 :goto_5

    :cond_e
    const/16 v0, 0x2a

    if-ne v6, v0, :cond_f

    if-eqz v4, :cond_f

    const/4 v0, 0x1

    const/4 v5, 0x6

    aget-object v5, v4, v5

    invoke-virtual {v5, v7}, La/c/i;->a(I)V

    goto/16 :goto_5

    :cond_f
    const/16 v0, 0x2b

    if-ne v6, v0, :cond_13

    if-eqz v4, :cond_13

    const/4 v0, 0x1

    const/4 v5, 0x7

    aget-object v5, v4, v5

    invoke-virtual {v5, v7}, La/c/i;->a(I)V

    goto/16 :goto_5

    :cond_10
    if-eqz v5, :cond_11

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 p0, 0x131

    invoke-static {p0}, Lpmsj/work/d/n;->h(I)V

    :cond_11
    sget-object p0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    if-ne v1, p0, :cond_12

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 p0, 0x1f

    invoke-static {p0}, Lpmsj/work/d/n;->h(I)V

    :cond_12
    sget-object p0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    if-ne v1, p0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object p0

    const/16 v0, 0x13e

    invoke-virtual {p0, v0}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ed;

    if-eqz p0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/ed;->ae()V

    goto/16 :goto_0

    :cond_13
    move v0, v5

    goto/16 :goto_5

    nop

    :sswitch_data_0
    .sparse-switch
        0x0 -> :sswitch_0
        0x19 -> :sswitch_1
        0x50 -> :sswitch_2
    .end sparse-switch

    :sswitch_data_1
    .sparse-switch
        0x2 -> :sswitch_5
        0x6 -> :sswitch_6
        0x7 -> :sswitch_e
        0xe -> :sswitch_7
        0xf -> :sswitch_8
        0x10 -> :sswitch_9
        0x11 -> :sswitch_a
        0x12 -> :sswitch_b
        0x13 -> :sswitch_c
        0x14 -> :sswitch_d
        0x16 -> :sswitch_f
        0x17 -> :sswitch_12
        0x1a -> :sswitch_10
        0x32 -> :sswitch_3
        0x33 -> :sswitch_11
        0x3e -> :sswitch_4
    .end sparse-switch
.end method

.method private static P(Lpmsj/work/main/w;)V
    .locals 10

    const/4 v9, 0x2

    const/16 v8, 0x13a

    const/4 v7, 0x1

    const/4 v3, 0x0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {v3}, Lpmsj/work/main/x;->a(B)Lpmsj/work/main/x;

    move-result-object v1

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    if-eqz v2, :cond_0

    :goto_1
    if-ge v3, v2, :cond_1

    mul-int/lit8 v4, v3, 0x2

    add-int/lit8 v4, v4, 0x2

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    invoke-static {v4}, Lpmsj/work/main/x;->d(I)I

    move-result v5

    mul-int/lit8 v6, v3, 0x2

    add-int/lit8 v6, v6, 0x3

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v6

    invoke-virtual {v1, v6, v4, v5}, Lpmsj/work/main/x;->a(BII)V

    add-int/lit8 v3, v3, 0x1

    goto :goto_1

    :cond_1
    const/4 v1, 0x3

    if-ne v1, v0, :cond_2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v8}, Lpmsj/work/d/n;->h(I)V

    :cond_2
    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/main/k;->o()V

    goto :goto_0

    :pswitch_2
    invoke-static {v7}, Lpmsj/work/main/x;->a(B)Lpmsj/work/main/x;

    move-result-object v1

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    if-eqz v2, :cond_0

    :goto_2
    if-ge v3, v2, :cond_4

    mul-int/lit8 v4, v3, 0x2

    add-int/lit8 v4, v4, 0x2

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    invoke-static {v4}, Lpmsj/work/main/x;->e(I)I

    move-result v5

    mul-int/lit8 v6, v3, 0x2

    add-int/lit8 v6, v6, 0x3

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v6

    invoke-virtual {v1, v6}, Lpmsj/work/main/x;->a(I)Lpmsj/work/main/r;

    move-result-object v6

    if-eqz v6, :cond_3

    invoke-virtual {v6, v7}, Lpmsj/work/main/r;->a(B)V

    :cond_3
    mul-int/lit8 v6, v3, 0x2

    add-int/lit8 v6, v6, 0x3

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v6

    invoke-virtual {v1, v6, v4, v5}, Lpmsj/work/main/x;->a(BII)V

    add-int/lit8 v3, v3, 0x1

    goto :goto_2

    :cond_4
    const/4 v1, 0x7

    if-ne v1, v0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v8}, Lpmsj/work/d/n;->h(I)V

    goto :goto_0

    :pswitch_3
    invoke-static {v9}, Lpmsj/work/main/x;->a(B)Lpmsj/work/main/x;

    move-result-object v1

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    if-eqz v2, :cond_0

    :goto_3
    if-ge v3, v2, :cond_6

    mul-int/lit8 v4, v3, 0x2

    add-int/lit8 v4, v4, 0x2

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    invoke-static {v4}, Lpmsj/work/main/x;->f(I)I

    move-result v5

    mul-int/lit8 v6, v3, 0x2

    add-int/lit8 v6, v6, 0x3

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v6

    invoke-virtual {v1, v6}, Lpmsj/work/main/x;->a(I)Lpmsj/work/main/r;

    move-result-object v6

    if-eqz v6, :cond_5

    invoke-virtual {v6, v9}, Lpmsj/work/main/r;->a(B)V

    :cond_5
    mul-int/lit8 v6, v3, 0x2

    add-int/lit8 v6, v6, 0x3

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v6

    invoke-virtual {v1, v6, v4, v5}, Lpmsj/work/main/x;->a(BII)V

    add-int/lit8 v3, v3, 0x1

    goto :goto_3

    :cond_6
    const/16 v1, 0xb

    if-ne v1, v0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v8}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_0
        :pswitch_1
        :pswitch_0
        :pswitch_0
        :pswitch_2
        :pswitch_2
        :pswitch_0
        :pswitch_0
        :pswitch_3
        :pswitch_3
    .end packed-switch
.end method

.method private static Q(Lpmsj/work/main/w;)V
    .locals 9

    const/4 v8, 0x0

    invoke-virtual {p0, v8}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    return-void

    :pswitch_0
    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    const/4 v2, 0x2

    sub-int/2addr v1, v2

    div-int/2addr v1, v0

    move v2, v8

    :goto_0
    if-ge v2, v0, :cond_0

    mul-int v3, v2, v1

    add-int/lit8 v4, v3, 0x2

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    add-int/lit8 v5, v3, 0x5

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    new-instance v6, Lpmsj/work/b/n;

    const v7, 0x200b20

    add-int/2addr v5, v7

    invoke-direct {v6, v4, v5, v8, v8}, Lpmsj/work/b/n;-><init>(IIZZ)V

    add-int/lit8 v4, v3, 0x6

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v4

    iput-object v4, v6, Lpmsj/work/b/n;->k:Ljava/lang/String;

    add-int/lit8 v4, v3, 0x3

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    add-int/lit8 v3, v3, 0x4

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v3

    invoke-virtual {v6, v4, v3}, Lpmsj/work/b/n;->c(II)V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v3

    invoke-virtual {v3, v6}, Lpmsj/work/b/m;->c(Lpmsj/work/b/n;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
    .end packed-switch
.end method

.method private static R(Lpmsj/work/main/w;)V
    .locals 5

    const/4 v1, 0x0

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    :goto_0
    if-ge v1, v0, :cond_1

    mul-int/lit8 v2, v1, 0x2

    add-int/lit8 v2, v2, 0x1

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    mul-int/lit8 v3, v1, 0x2

    add-int/lit8 v3, v3, 0x2

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v3

    invoke-static {v2, v3}, Lpmsj/work/b/p;->a(IB)V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4, v2}, Lpmsj/work/b/m;->l(I)Lpmsj/work/b/t;

    move-result-object v2

    if-eqz v2, :cond_0

    iput-byte v3, v2, Lpmsj/work/b/t;->h:B

    invoke-virtual {v2}, Lpmsj/work/b/t;->a()V

    :cond_0
    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    :cond_1
    return-void
.end method

.method private static S(Lpmsj/work/main/w;)V
    .locals 5

    const/4 v3, 0x0

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    invoke-virtual {v0}, La/c/i;->b()I

    move-result v0

    if-nez v0, :cond_1

    :cond_0
    return-void

    :cond_1
    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    const/4 v2, 0x1

    sub-int/2addr v1, v2

    div-int/2addr v1, v0

    move v2, v3

    :goto_0
    if-ge v2, v0, :cond_0

    mul-int v3, v2, v1

    add-int/lit8 v3, v3, 0x1

    invoke-virtual {p0, v1, v3}, Lpmsj/work/main/w;->a(II)La/c/a;

    move-result-object v3

    sget-object v4, Lpmsj/work/b/p;->a:Ljava/util/Vector;

    invoke-virtual {v4, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_0
.end method

.method private static T(Lpmsj/work/main/w;)V
    .locals 6

    const/4 v5, 0x0

    const/4 v4, 0x1

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->z()Ljava/util/Vector;

    move-result-object v0

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    const/16 v1, 0x14

    if-lt v0, v1, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v1}, Lpmsj/work/b/ab;->u()I

    move-result v1

    if-eq v0, v1, :cond_0

    const/16 v0, 0x16

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/v;->H(I)I

    move-result v0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    const/4 v3, 0x6

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v3

    invoke-virtual {v1, v2, v0, v3}, Lpmsj/work/b/m;->a(III)Lpmsj/work/b/v;

    move-result-object v0

    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    invoke-virtual {v0}, Lpmsj/work/b/v;->B()V

    move v2, v5

    :goto_1
    if-ge v2, v1, :cond_2

    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v3

    invoke-virtual {v0, v2, v3}, Lpmsj/work/b/v;->a(BLjava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    int-to-byte v2, v2

    goto :goto_1

    :cond_2
    invoke-virtual {v0}, Lpmsj/work/b/v;->r()V

    const/4 v1, 0x4

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    const/4 v2, 0x5

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    invoke-virtual {v0, v1, v2}, Lpmsj/work/b/v;->c(II)V

    invoke-virtual {v0}, Lpmsj/work/b/v;->I()V

    invoke-virtual {v0}, Lpmsj/work/b/v;->P()V

    invoke-virtual {v0}, Lpmsj/work/b/v;->Q()V

    const/16 v1, 0x19

    invoke-virtual {v0, v1}, Lpmsj/work/b/v;->f(B)I

    move-result v1

    invoke-virtual {v0, v1, v5}, Lpmsj/work/b/v;->g(II)V

    const/high16 v1, 0x2000000

    invoke-virtual {v0, v1}, Lpmsj/work/b/v;->a(I)Z

    move-result v1

    if-eqz v1, :cond_3

    const v1, 0x2143a0

    invoke-virtual {v0, v1, v4}, Lpmsj/work/b/v;->b(IZ)La/a/d;

    :cond_3
    const/high16 v1, 0x20000

    invoke-virtual {v0, v1}, Lpmsj/work/b/v;->a(I)Z

    move-result v1

    if-eqz v1, :cond_4

    const v1, 0x208050

    invoke-virtual {v0, v1, v4}, Lpmsj/work/b/v;->b(IZ)La/a/d;

    :cond_4
    const/high16 v1, 0x1000000

    invoke-virtual {v0, v1}, Lpmsj/work/b/v;->a(I)Z

    move-result v1

    if-eqz v1, :cond_5

    const v1, 0x21b8d0

    invoke-virtual {v0, v1, v4}, Lpmsj/work/b/v;->b(IZ)La/a/d;

    :cond_5
    invoke-virtual {v0}, Lpmsj/work/b/v;->af()Z

    move-result v1

    if-eqz v1, :cond_6

    const v1, 0x9c40

    invoke-virtual {v0, v1, v4}, Lpmsj/work/b/v;->c(IZ)La/a/d;

    :cond_6
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->Z()Z

    move-result v1

    if-eqz v1, :cond_0

    invoke-virtual {v0}, Lpmsj/work/b/v;->u()I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/aa;->c(I)Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/b/aa;->h()V

    goto/16 :goto_0
.end method

.method private static U(Lpmsj/work/main/w;)V
    .locals 10

    const/4 v9, 0x5

    const/4 v8, 0x0

    invoke-virtual {p0, v8}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/main/b;->g()I

    move-result v1

    if-eq v0, v1, :cond_0

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "processBattleAckCmd\u548c\u5ba2\u6237\u7aef\u5f53\u524d\u56de\u5408\u4e0d\u540c, \u5ba2\u6237\u7aef:"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/main/b;->g()I

    move-result v2

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v2, ",\u6d88\u606f:"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {v1}, Lpmsj/work/main/b;->a(Ljava/lang/String;)V

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/main/b;->a(I)V

    :cond_0
    new-instance v0, Lpmsj/work/b/b;

    invoke-direct {v0}, Lpmsj/work/b/b;-><init>()V

    const/4 v1, 0x1

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    iput v1, v0, Lpmsj/work/b/b;->a:I

    const/4 v1, 0x2

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    iput v1, v0, Lpmsj/work/b/b;->b:I

    const/4 v1, 0x3

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    iput-byte v1, v0, Lpmsj/work/b/b;->c:B

    const/4 v1, 0x4

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    iput v1, v0, Lpmsj/work/b/b;->d:I

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    iput-byte v1, v0, Lpmsj/work/b/b;->e:B

    const/4 v1, 0x6

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    iput v1, v0, Lpmsj/work/b/b;->f:I

    const/4 v1, 0x7

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    iput v1, v0, Lpmsj/work/b/b;->g:I

    const/16 v1, 0x8

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v1

    iput-object v1, v0, Lpmsj/work/b/b;->h:Ljava/lang/String;

    const/16 v1, 0x9

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    move v2, v8

    :goto_0
    if-ge v2, v1, :cond_2

    mul-int/lit8 v3, v2, 0x5

    add-int/lit8 v3, v3, 0xa

    new-instance v4, La/c/a;

    invoke-direct {v4, v9}, La/c/a;-><init>(I)V

    move v5, v3

    move v3, v8

    :goto_1
    if-ge v3, v9, :cond_1

    iget-object v6, v4, La/c/a;->a:[La/c/i;

    add-int/lit8 v7, v5, 0x1

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v5

    aput-object v5, v6, v3

    add-int/lit8 v3, v3, 0x1

    move v5, v7

    goto :goto_1

    :cond_1
    iget-object v3, v0, Lpmsj/work/b/b;->i:Ljava/util/Vector;

    invoke-virtual {v3, v4}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_0

    :cond_2
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/main/b;->a(Lpmsj/work/b/b;)V

    return-void
.end method

.method private static V(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x1

    const/4 v0, 0x0

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    sparse-switch v0, :sswitch_data_0

    :cond_0
    :goto_0
    return-void

    :sswitch_0
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/main/b;->g:Lpmsj/work/a/l;

    invoke-virtual {v0, v1}, Lpmsj/work/a/l;->b(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Lpmsj/work/b/h;

    if-eqz p0, :cond_0

    invoke-virtual {p0, v2}, Lpmsj/work/b/h;->a(Z)V

    goto :goto_0

    :sswitch_1
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->u()I

    move-result v0

    if-ne v1, v0, :cond_1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x14

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/j;

    if-eqz p0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/j;->j()V

    invoke-static {}, Lpmsj/work/main/b;->c()V

    goto :goto_0

    :cond_1
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/main/b;->h:Lpmsj/work/a/l;

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/main/b;->h:Lpmsj/work/a/l;

    invoke-virtual {v0, v1}, Lpmsj/work/a/l;->c(I)Ljava/lang/Object;

    goto :goto_0

    nop

    :sswitch_data_0
    .sparse-switch
        0xa -> :sswitch_1
        0x65 -> :sswitch_0
    .end sparse-switch
.end method

.method private static W(Lpmsj/work/main/w;)V
    .locals 5

    const/4 v3, 0x0

    const/4 v4, 0x1

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    const/4 v1, 0x3

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    new-instance v2, Lpmsj/work/b/q;

    invoke-direct {v2, v0, v1}, Lpmsj/work/b/q;-><init>(II)V

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    move v1, v3

    :goto_0
    if-ge v1, v0, :cond_0

    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v3

    invoke-virtual {v2, v1, v3}, Lpmsj/work/b/q;->a(BLjava/lang/Object;)V

    add-int/lit8 v1, v1, 0x1

    int-to-byte v1, v1

    goto :goto_0

    :cond_0
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0, v2}, Lpmsj/work/b/m;->a(Lpmsj/work/b/q;)V

    const/high16 v0, 0x20000

    invoke-virtual {v2, v0}, Lpmsj/work/b/q;->a(I)Z

    move-result v0

    if-eqz v0, :cond_1

    const v0, 0x208050

    invoke-virtual {v2, v0, v4}, Lpmsj/work/b/q;->b(IZ)La/a/d;

    :cond_1
    const/high16 v0, 0x800000

    invoke-virtual {v2, v0}, Lpmsj/work/b/q;->a(I)Z

    move-result v0

    if-eqz v0, :cond_2

    const v0, 0x9c40

    invoke-virtual {v2, v0, v4}, Lpmsj/work/b/q;->c(IZ)La/a/d;

    :cond_2
    invoke-virtual {v2, v4}, Lpmsj/work/b/q;->f(B)I

    move-result v0

    const/4 v1, 0x2

    invoke-virtual {v2, v1}, Lpmsj/work/b/q;->f(B)I

    move-result v1

    invoke-virtual {v2, v0, v1}, Lpmsj/work/b/q;->c(II)V

    return-void
.end method

.method private static X(Lpmsj/work/main/w;)V
    .locals 5

    const/4 v4, 0x3

    const/4 v3, 0x0

    new-instance v0, Lpmsj/work/b/t;

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    invoke-direct {v0, v1, v2}, Lpmsj/work/b/t;-><init>(II)V

    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    move v2, v3

    :goto_0
    if-ge v2, v1, :cond_0

    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v3

    invoke-virtual {v0, v2, v3}, Lpmsj/work/b/t;->a(BLjava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    int-to-byte v2, v2

    goto :goto_0

    :cond_0
    const/4 v1, 0x7

    invoke-virtual {v0, v1}, Lpmsj/work/b/t;->f(B)I

    move-result v1

    and-int/lit8 v1, v1, 0x1

    if-eqz v1, :cond_1

    invoke-virtual {v0, v4}, Lpmsj/work/b/t;->q(I)V

    iget-object v1, v0, Lpmsj/work/b/t;->o:La/a/d;

    if-eqz v1, :cond_1

    iget-object v1, v0, Lpmsj/work/b/t;->o:La/a/d;

    const/4 v2, 0x2

    invoke-virtual {v1, v2}, La/a/d;->a(B)V

    :cond_1
    invoke-virtual {v0}, Lpmsj/work/b/t;->b()V

    invoke-virtual {v0}, Lpmsj/work/b/t;->d()V

    const/4 v1, 0x5

    invoke-virtual {v0, v1}, Lpmsj/work/b/t;->f(B)I

    move-result v1

    if-lez v1, :cond_2

    div-int/lit8 v2, v1, 0x64

    mul-int/lit8 v2, v2, 0x64

    rem-int/lit8 v1, v1, 0x64

    const/4 v3, 0x1

    invoke-virtual {v0, v2, v1, v3}, Lpmsj/work/b/t;->a(IIZ)La/a/d;

    :cond_2
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/b/m;->a(Lpmsj/work/b/t;)V

    return-void
.end method

.method private static Y(Lpmsj/work/main/w;)V
    .locals 5

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    add-int/lit8 v0, v0, 0x1

    add-int/lit8 v1, v0, 0x1

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    move v4, v2

    move v2, v1

    move v1, v4

    :goto_0
    if-ge v1, v0, :cond_0

    add-int/lit8 v3, v2, 0x1

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    invoke-static {v2}, La/a/f;->b(I)V

    add-int/lit8 v1, v1, 0x1

    move v2, v3

    goto :goto_0

    :cond_0
    return-void
.end method

.method private static Z(Lpmsj/work/main/w;)V
    .locals 11

    const/16 v10, 0x8

    const/4 v6, 0x7

    const/4 v9, 0x4

    const/4 v8, 0x5

    const/4 v7, 0x0

    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    const/4 v1, 0x0

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    const/4 v2, 0x1

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v3

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->a(I)B

    move-result v5

    packed-switch v5, :pswitch_data_0

    :pswitch_0
    invoke-static {v2, v3}, Lpmsj/work/b/a;->a(II)Lpmsj/work/b/j;

    move-result-object v1

    move-object v2, v1

    :goto_0
    if-nez v2, :cond_3

    :cond_0
    :goto_1
    return-void

    :pswitch_1
    invoke-static {v2, v3}, Lpmsj/work/b/a;->a(II)Lpmsj/work/b/j;

    move-result-object v1

    sparse-switch v4, :sswitch_data_0

    invoke-virtual {v1}, Lpmsj/work/b/j;->b()Z

    move-result v2

    if-eqz v2, :cond_d

    invoke-static {}, Lpmsj/work/b/a;->g()Ljava/util/Vector;

    move-result-object v2

    invoke-virtual {v2, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    move-object v2, v1

    goto :goto_0

    :sswitch_0
    invoke-static {v2, v3}, Lpmsj/work/b/a;->a(II)Lpmsj/work/b/j;

    move-result-object v1

    move-object v2, v1

    goto :goto_0

    :sswitch_1
    invoke-static {}, Lpmsj/work/b/a;->e()Ljava/util/Vector;

    move-result-object v2

    invoke-virtual {v2, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    move-object v2, v1

    goto :goto_0

    :sswitch_2
    invoke-static {}, Lpmsj/work/b/a;->f()Ljava/util/Vector;

    move-result-object v2

    invoke-virtual {v2, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    move-object v2, v1

    goto :goto_0

    :pswitch_2
    sparse-switch v4, :sswitch_data_1

    invoke-static {v3}, Lpmsj/work/b/j;->g(I)Z

    move-result v3

    if-eqz v3, :cond_c

    invoke-static {v2}, Lpmsj/work/b/a;->d(I)Lpmsj/work/b/j;

    move-result-object v1

    if-nez v1, :cond_2

    invoke-static {}, Lpmsj/work/b/a;->g()Ljava/util/Vector;

    move-result-object v1

    invoke-static {v2, v1}, Lpmsj/work/b/a;->a(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-result-object v1

    move-object v2, v1

    goto :goto_0

    :sswitch_3
    invoke-static {v2, v3}, Lpmsj/work/b/a;->a(II)Lpmsj/work/b/j;

    move-result-object v1

    move-object v2, v1

    goto :goto_0

    :sswitch_4
    invoke-static {}, Lpmsj/work/b/a;->e()Ljava/util/Vector;

    move-result-object v1

    invoke-static {v2, v1}, Lpmsj/work/b/a;->a(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-result-object v1

    if-nez v1, :cond_1

    invoke-static {v2, v3}, Lpmsj/work/b/a;->a(II)Lpmsj/work/b/j;

    move-result-object v1

    invoke-static {}, Lpmsj/work/b/a;->e()Ljava/util/Vector;

    move-result-object v3

    invoke-virtual {v3, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_1
    invoke-static {}, Lpmsj/work/b/a;->g()Ljava/util/Vector;

    move-result-object v3

    invoke-static {v2, v3}, Lpmsj/work/b/a;->b(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-object v2, v1

    goto :goto_0

    :sswitch_5
    invoke-static {}, Lpmsj/work/b/a;->f()Ljava/util/Vector;

    move-result-object v1

    invoke-static {v2, v1}, Lpmsj/work/b/a;->a(ILjava/util/Vector;)Lpmsj/work/b/j;

    move-result-object v1

    if-nez v1, :cond_d

    invoke-static {v2, v3}, Lpmsj/work/b/a;->a(II)Lpmsj/work/b/j;

    move-result-object v1

    invoke-static {}, Lpmsj/work/b/a;->f()Ljava/util/Vector;

    move-result-object v2

    invoke-virtual {v2, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    move-object v2, v1

    goto/16 :goto_0

    :cond_2
    invoke-static {}, Lpmsj/work/b/a;->g()Ljava/util/Vector;

    move-result-object v2

    invoke-virtual {v2, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    move-object v2, v1

    goto/16 :goto_0

    :cond_3
    const/4 v1, 0x2

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    iput-short v1, v2, Lpmsj/work/b/j;->g:S

    const/4 v1, 0x3

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    iput-short v1, v2, Lpmsj/work/b/j;->h:S

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    iput-byte v1, v2, Lpmsj/work/b/j;->k:B

    invoke-virtual {p0, v8}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    iput v1, v2, Lpmsj/work/b/j;->m:I

    const/4 v1, 0x6

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v2, Lpmsj/work/b/j;->i:I

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v2, Lpmsj/work/b/j;->f:I

    invoke-virtual {p0, v10}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v1

    iput-object v1, v2, Lpmsj/work/b/j;->o:Ljava/lang/String;

    const/16 v1, 0x9

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    iput-short v1, v2, Lpmsj/work/b/j;->l:S

    const/16 v1, 0xa

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    iput-short v1, v2, Lpmsj/work/b/j;->j:S

    const/16 v1, 0xb

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    iput-byte v1, v2, Lpmsj/work/b/j;->n:B

    const/16 v1, 0xc

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    iput-short v1, v2, Lpmsj/work/b/j;->q:S

    const/16 v1, 0xd

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v2, Lpmsj/work/b/j;->p:I

    const/16 v1, 0xe

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    iput-short v1, v2, Lpmsj/work/b/j;->s:S

    const/16 v1, 0xf

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    iput-short v1, v2, Lpmsj/work/b/j;->t:S

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v5

    iput-wide v5, v2, Lpmsj/work/b/j;->r:J

    iget v1, v2, Lpmsj/work/b/j;->f:I

    invoke-static {v1}, Lpmsj/work/b/j;->i(I)Z

    move-result v1

    if-eqz v1, :cond_7

    const/16 v1, 0x10

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v2, Lpmsj/work/b/j;->u:I

    :cond_4
    iget v1, v2, Lpmsj/work/b/j;->f:I

    invoke-static {v1}, Lpmsj/work/b/j;->h(I)Z

    move-result v1

    if-eqz v1, :cond_5

    move-object v0, v2

    check-cast v0, Lpmsj/work/b/r;

    move-object v3, v0

    const/16 v1, 0x27

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v3, Lpmsj/work/b/r;->x:I

    const/16 v1, 0x28

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v3, Lpmsj/work/b/r;->y:I

    const/16 v1, 0x29

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v3, Lpmsj/work/b/r;->z:I

    const/16 v1, 0x2a

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v3, Lpmsj/work/b/r;->A:I

    const/16 v1, 0x2b

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v3, Lpmsj/work/b/r;->B:I

    const/16 v1, 0x2c

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    iput-byte v1, v3, Lpmsj/work/b/r;->C:B

    const/16 v1, 0x2d

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    iput-byte v1, v3, Lpmsj/work/b/r;->D:B

    const/16 v1, 0x2e

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    iput v1, v3, Lpmsj/work/b/r;->E:I

    const/16 v1, 0x2f

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v1

    iput-object v1, v3, Lpmsj/work/b/r;->F:Ljava/lang/String;

    :cond_5
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v8}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v9}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v1

    check-cast v1, Lpmsj/work/e/ea;

    if-eqz v1, :cond_6

    const/16 v3, -0x37

    if-ne v3, v4, :cond_b

    invoke-virtual {v1, v2}, Lpmsj/work/e/ea;->c(Lpmsj/work/b/j;)V

    :cond_6
    :goto_2
    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    packed-switch v1, :pswitch_data_1

    goto/16 :goto_1

    :pswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v3, 0x10

    invoke-virtual {v1, v3}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/eu;

    if-eqz p0, :cond_0

    invoke-virtual {p0, v2}, Lpmsj/work/e/eu;->b(Lpmsj/work/b/j;)V

    goto/16 :goto_1

    :cond_7
    invoke-virtual {v2}, Lpmsj/work/b/j;->c()Z

    move-result v1

    if-eqz v1, :cond_4

    move-object v0, v2

    check-cast v0, Lpmsj/work/b/g;

    move-object v1, v0

    move v3, v7

    :goto_3
    if-ge v3, v10, :cond_8

    add-int/lit8 v5, v3, 0x10

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->b(I)S

    move-result v5

    invoke-virtual {v1, v3, v5}, Lpmsj/work/b/g;->a(BS)V

    add-int/lit8 v3, v3, 0x1

    int-to-byte v3, v3

    goto :goto_3

    :cond_8
    move v3, v7

    :goto_4
    if-ge v3, v8, :cond_9

    add-int/lit8 v5, v3, 0x18

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->a(I)B

    move-result v5

    invoke-virtual {v1, v3, v5}, Lpmsj/work/b/g;->a(BB)V

    add-int/lit8 v3, v3, 0x1

    int-to-byte v3, v3

    goto :goto_4

    :cond_9
    move v3, v7

    :goto_5
    if-ge v3, v8, :cond_a

    add-int/lit8 v5, v3, 0x1d

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->a(I)B

    move-result v5

    invoke-virtual {v1, v3, v5}, Lpmsj/work/b/g;->b(BB)V

    add-int/lit8 v3, v3, 0x1

    int-to-byte v3, v3

    goto :goto_5

    :cond_a
    move v3, v7

    :goto_6
    if-ge v3, v8, :cond_4

    add-int/lit8 v5, v3, 0x22

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    invoke-virtual {v1, v3, v5}, Lpmsj/work/b/g;->a(BI)V

    add-int/lit8 v3, v3, 0x1

    int-to-byte v3, v3

    goto :goto_6

    :cond_b
    iget v3, v2, Lpmsj/work/b/j;->e:I

    invoke-virtual {v1, v3}, Lpmsj/work/e/ea;->E(I)V

    goto :goto_2

    :cond_c
    move-object v2, v1

    goto/16 :goto_0

    :cond_d
    move-object v2, v1

    goto/16 :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_0
        :pswitch_2
    .end packed-switch

    :sswitch_data_0
    .sparse-switch
        -0x37 -> :sswitch_0
        0x32 -> :sswitch_1
        0x33 -> :sswitch_2
    .end sparse-switch

    :sswitch_data_1
    .sparse-switch
        -0x37 -> :sswitch_3
        0x32 -> :sswitch_4
        0x33 -> :sswitch_5
    .end sparse-switch

    :pswitch_data_1
    .packed-switch 0x2
        :pswitch_3
    .end packed-switch
.end method

.method private static a(La/c/a;)I
    .locals 6

    const/4 v5, -0x1

    const/4 v4, 0x0

    sget-object v0, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    if-nez v0, :cond_0

    move v0, v5

    :goto_0
    return v0

    :cond_0
    sget-object v0, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v1

    move v2, v4

    :goto_1
    if-ge v2, v1, :cond_2

    sget-object v0, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-virtual {p0, v4}, La/c/a;->a(I)I

    move-result v3

    invoke-virtual {v0, v4}, La/c/a;->a(I)I

    move-result v0

    if-ne v3, v0, :cond_1

    sget-object v0, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    invoke-virtual {v0, p0, v2}, Ljava/util/Vector;->setElementAt(Ljava/lang/Object;I)V

    move v0, v2

    goto :goto_0

    :cond_1
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_1

    :cond_2
    move v0, v5

    goto :goto_0
.end method

.method public static a(BIIS)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    const/16 v1, 0x409

    invoke-virtual {v0, v1}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->d(I)V

    invoke-virtual {v0, p0}, La/c/r;->b(I)V

    invoke-virtual {v0, p2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->c(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(I)V
    .locals 2

    const/16 v0, 0x420

    const/4 v1, 0x1

    invoke-static {v0, v1, p0}, Lpmsj/work/main/w;->a(IBI)V

    return-void
.end method

.method public static a(II)V
    .locals 2

    const/16 v0, 0x408

    const/4 v1, 0x3

    invoke-static {v0, v1, p0, p1}, Lpmsj/work/main/w;->a(IBII)V

    return-void
.end method

.method public static a(IISS)V
    .locals 3

    const/4 v2, 0x0

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    const/16 v1, 0x7ef

    invoke-virtual {v0, v1}, La/c/r;->a(I)V

    invoke-virtual {v0, p1}, La/c/r;->d(I)V

    invoke-virtual {v0, v2}, La/c/r;->d(I)V

    invoke-virtual {v0, p2}, La/c/r;->c(I)V

    invoke-virtual {v0, p3}, La/c/r;->c(I)V

    invoke-virtual {v0, p0}, La/c/r;->c(I)V

    invoke-virtual {v0, v2}, La/c/r;->c(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(Ljava/io/DataInputStream;)V
    .locals 19

    const/4 v6, 0x3

    const/4 v14, 0x4

    const/4 v13, 0x2

    const/4 v8, 0x1

    const/4 v7, 0x0

    invoke-virtual/range {p0 .. p0}, Ljava/io/DataInputStream;->readShort()S

    move-result v4

    invoke-static {}, Lpmsj/work/main/w;->a()Lpmsj/work/main/w;

    move-result-object v18

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v5, v0

    invoke-virtual {v5}, Ljava/util/Vector;->removeAllElements()V

    :goto_0
    :try_start_0
    invoke-virtual/range {p0 .. p0}, Ljava/io/DataInputStream;->read()I

    move-result v5

    int-to-byte v5, v5

    const/4 v9, -0x1

    if-eq v5, v9, :cond_0

    packed-switch v5, :pswitch_data_0

    goto :goto_0

    :pswitch_0
    invoke-virtual/range {p0 .. p0}, Ljava/io/DataInputStream;->readShort()S

    move-result v5

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v9, v0

    new-instance v10, La/c/o;

    invoke-direct {v10, v5}, La/c/o;-><init>(S)V

    invoke-virtual {v9, v10}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V
    :try_end_0
    .catch Ljava/io/IOException; {:try_start_0 .. :try_end_0} :catch_0

    goto :goto_0

    :catch_0
    move-exception v5

    invoke-virtual {v5}, Ljava/io/IOException;->printStackTrace()V

    :cond_0
    const/16 v5, 0x3f4

    if-eq v5, v4, :cond_2

    sget-object v5, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v9, Ljava/lang/StringBuilder;

    invoke-direct {v9}, Ljava/lang/StringBuilder;-><init>()V

    const-string v10, "cmd="

    invoke-virtual {v9, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v9

    const/16 v10, 0x3e8

    sub-int v10, v4, v10

    invoke-virtual {v9, v10}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v9

    const-string v10, ":"

    invoke-virtual {v9, v10}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v9

    invoke-virtual {v9}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v9

    invoke-virtual {v5, v9}, Ljava/io/PrintStream;->print(Ljava/lang/String;)V

    move v5, v7

    :goto_1
    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v9, v0

    invoke-virtual {v9}, Ljava/util/Vector;->size()I

    move-result v9

    if-ge v5, v9, :cond_1

    sget-object v9, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v10, Ljava/lang/StringBuilder;

    invoke-direct {v10}, Ljava/lang/StringBuilder;-><init>()V

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v11, v0

    invoke-virtual {v11, v5}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v11

    invoke-virtual {v11}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v11

    invoke-virtual {v10, v11}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v10

    const-string v11, ","

    invoke-virtual {v10, v11}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v10

    invoke-virtual {v10}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v10

    invoke-virtual {v9, v10}, Ljava/io/PrintStream;->print(Ljava/lang/String;)V

    add-int/lit8 v5, v5, 0x1

    goto :goto_1

    :pswitch_1
    :try_start_1
    invoke-virtual/range {p0 .. p0}, Ljava/io/DataInputStream;->readByte()B

    move-result v5

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v9, v0

    new-instance v10, La/c/h;

    invoke-direct {v10, v5}, La/c/h;-><init>(B)V

    invoke-virtual {v9, v10}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_0

    :pswitch_2
    invoke-virtual/range {p0 .. p0}, Ljava/io/DataInputStream;->readShort()S

    move-result v5

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v9, v0

    new-instance v10, La/c/o;

    invoke-direct {v10, v5}, La/c/o;-><init>(S)V

    invoke-virtual {v9, v10}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_0

    :pswitch_3
    invoke-virtual/range {p0 .. p0}, Ljava/io/DataInputStream;->readInt()I

    move-result v5

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v9, v0

    new-instance v10, La/c/m;

    invoke-direct {v10, v5}, La/c/m;-><init>(I)V

    invoke-virtual {v9, v10}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_0

    :pswitch_4
    new-instance v5, La/c/p;

    invoke-static/range {p0 .. p0}, La/c/d;->a(Ljava/io/DataInputStream;)Ljava/lang/String;

    move-result-object v9

    invoke-direct {v5, v9}, La/c/p;-><init>(Ljava/lang/String;)V

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v9, v0

    invoke-virtual {v9, v5}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_0

    :pswitch_5
    invoke-virtual/range {p0 .. p0}, Ljava/io/DataInputStream;->readShort()S

    move-result v5

    invoke-static {v5}, La/c/x;->a(S)I

    move-result v5

    new-array v5, v5, [B

    move-object/from16 v0, p0

    move-object v1, v5

    invoke-virtual {v0, v1}, Ljava/io/DataInputStream;->read([B)I

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v9, v0

    invoke-virtual {v9, v5}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_0

    :pswitch_6
    invoke-virtual/range {p0 .. p0}, Ljava/io/DataInputStream;->readByte()B

    move-result v5

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v9, v0

    new-instance v10, La/c/h;

    invoke-direct {v10, v5}, La/c/h;-><init>(B)V

    invoke-virtual {v9, v10}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto/16 :goto_0

    :pswitch_7
    invoke-virtual/range {p0 .. p0}, Ljava/io/DataInputStream;->readLong()J

    move-result-wide v9

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v5, v0

    new-instance v11, La/c/n;

    invoke-direct {v11, v9, v10}, La/c/n;-><init>(J)V

    invoke-virtual {v5, v11}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V
    :try_end_1
    .catch Ljava/io/IOException; {:try_start_1 .. :try_end_1} :catch_0

    goto/16 :goto_0

    :cond_1
    sget-object v5, Ljava/lang/System;->out:Ljava/io/PrintStream;

    const-string v9, "\n"

    invoke-virtual {v5, v9}, Ljava/io/PrintStream;->print(Ljava/lang/String;)V

    :cond_2
    sparse-switch v4, :sswitch_data_0

    new-instance v5, La/c/p;

    new-instance v6, Ljava/lang/StringBuilder;

    invoke-direct {v6}, Ljava/lang/StringBuilder;-><init>()V

    const-string v7, "\u6709\u53d1\u73b0\u5ba2\u6237\u7aef\u672a\u5b9a\u4e49\u7684\u6d88\u606f\u7c7b\u578b\uff0c \u7c7b\u578b\uff1d"

    invoke-virtual {v6, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v6

    invoke-virtual {v6, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    invoke-direct {v5, v4}, La/c/p;-><init>(Ljava/lang/String;)V

    invoke-static {v5}, Lpmsj/work/main/w;->a(La/c/i;)V

    :cond_3
    :goto_2
    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v4, v0

    invoke-virtual {v4}, Ljava/util/Vector;->removeAllElements()V

    return-void

    :sswitch_0
    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    packed-switch v4, :pswitch_data_1

    goto :goto_2

    :pswitch_8
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0xc

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_2

    :pswitch_9
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x9

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x9

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/as;

    sget-object v4, Lpmsj/work/b/f;->A:Lpmsj/work/a/l;

    if-nez v4, :cond_4

    new-instance v4, Lpmsj/work/a/l;

    invoke-direct {v4}, Lpmsj/work/a/l;-><init>()V

    sput-object v4, Lpmsj/work/b/f;->A:Lpmsj/work/a/l;

    :cond_4
    sget-object v4, Lpmsj/work/b/f;->A:Lpmsj/work/a/l;

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v6

    invoke-virtual {v4, v5, v6}, Lpmsj/work/a/l;->a(ILjava/lang/Object;)Ljava/lang/Object;

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v4

    move-object/from16 v0, p0

    move-object v1, v4

    invoke-virtual {v0, v1}, Lpmsj/work/e/as;->g(Ljava/lang/String;)V

    const-string v4, "\u5e2e\u52a9"

    move-object/from16 v0, p0

    move-object v1, v4

    invoke-virtual {v0, v1}, Lpmsj/work/e/as;->e(Ljava/lang/String;)V

    goto :goto_2

    :sswitch_1
    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v5

    packed-switch v4, :pswitch_data_2

    :pswitch_a
    goto/16 :goto_2

    :pswitch_b
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x72

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const-string v5, "\u606d\u559c\u60a8\uff0c\u6ce8\u518c\u6210\u529f\u3002"

    const/16 v6, 0xfa0

    invoke-virtual {v4, v5, v6}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x136

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/bd;

    if-eqz p0, :cond_3

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/e/bd;->i()V

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/e/bd;->k()V

    goto/16 :goto_2

    :pswitch_c
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const-string v5, "\u8d26\u53f7\u6216\u5bc6\u7801\u4e2d\u6709\u975e\u6cd5\u5b57\u7b26\u3002"

    const/16 v6, 0xfa0

    invoke-virtual {v4, v5, v6}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    goto/16 :goto_2

    :pswitch_d
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const-string v5, "\u5df2\u5b58\u5728\u6b64\u8d26\u53f7\uff0c\u8bf7\u91cd\u65b0\u8f93\u5165\u8d26\u53f7\u540d\u3002"

    const/16 v6, 0xfa0

    invoke-virtual {v4, v5, v6}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    goto/16 :goto_2

    :pswitch_e
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x136

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/bd;

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v4

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v5

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v6

    move-object/from16 v0, p0

    move-object v1, v4

    move-object v2, v5

    invoke-virtual {v0, v1, v2}, Lpmsj/work/e/bd;->b(Ljava/lang/String;Ljava/lang/String;)V

    invoke-static {v4, v5, v8, v8}, Lpmsj/work/main/f;->a(Ljava/lang/String;Ljava/lang/String;II)V

    sget v7, Lpmsj/work/main/i;->m:I

    sget v8, Lpmsj/work/main/i;->n:I

    or-int/2addr v7, v8

    invoke-static {v7}, Lpmsj/work/main/i;->c(I)V

    invoke-static {}, Lpmsj/work/main/c;->a()Lpmsj/work/main/c;

    const/4 v7, 0x0

    invoke-static {v7, v4, v5}, Lpmsj/work/main/c;->a(Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    new-instance v7, Ljava/lang/StringBuffer;

    invoke-direct {v7}, Ljava/lang/StringBuffer;-><init>()V

    const-string v8, "\u606d\u559c\u60a8\uff0c\u6ce8\u518c\u6210\u529f\u3002"

    invoke-virtual {v7, v8}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/16 v8, 0x5f

    invoke-virtual {v7, v8}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    const-string v8, "\u8d26\u53f7\uff1a"

    invoke-virtual {v7, v8}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v8, "*3"

    invoke-virtual {v7, v8}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/16 v4, 0x5f

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    const-string v4, "\u5bc6\u7801\uff1a"

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v4, "*3"

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v7, v5}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/16 v4, 0x5f

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    invoke-virtual {v6}, Ljava/lang/String;->length()I

    move-result v4

    if-lez v4, :cond_5

    const-string v4, "\u670d\u52a1\u5668\uff1a"

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v4, "*3"

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v7, v6}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/16 v4, 0x5f

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    :goto_3
    const-string v4, "*2\u8bf7\u7262\u8bb0\u4f60\u7684\u8d26\u53f7\u5bc6\u7801\uff01"

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v7}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v4

    sput-object v4, Lpmsj/work/main/e;->f:Ljava/lang/String;

    goto/16 :goto_2

    :cond_5
    const-string v4, "*2\u63d0\u793a\uff1a\u53ef\u767b\u5f55\u6700\u65b0\u670d\u52a1\u5668\uff01"

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/16 v4, 0x5f

    invoke-virtual {v7, v4}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    goto :goto_3

    :pswitch_f
    move-object/from16 v0, v18

    move v1, v14

    move v2, v8

    invoke-virtual {v0, v1, v2}, Lpmsj/work/main/w;->a(II)La/c/a;

    move-result-object v4

    invoke-static {}, Lpmsj/work/main/c;->a()Lpmsj/work/main/c;

    invoke-static {v4}, Lpmsj/work/main/c;->a(La/c/a;)V

    invoke-static {}, Lpmsj/work/main/f;->b()V

    goto/16 :goto_2

    :pswitch_10
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x72

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const-string v5, "\u5bc6\u7801\u4fee\u6539\u6210\u529f"

    const/16 v6, 0xfa0

    invoke-virtual {v4, v5, v6}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    goto/16 :goto_2

    :pswitch_11
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const-string v5, "\u9519\u8bef\u7684\u8d26\u53f7\u6216\u5bc6\u7801"

    const/16 v6, 0xfa0

    invoke-virtual {v4, v5, v6}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    goto/16 :goto_2

    :pswitch_12
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v6, 0xfa0

    invoke-virtual {v4, v5, v6}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    goto/16 :goto_2

    :sswitch_2
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->K(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_3
    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x192

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v8

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_4
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    packed-switch v4, :pswitch_data_3

    :pswitch_13
    goto/16 :goto_2

    :pswitch_14
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const-string v5, "\u60a8\u5df2\u7ecf\u6b7b\u4ea1\uff0c\u8981\u539f\u5730\u590d\u6d3b\u5417\uff1f"

    const/16 v6, 0x23

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v7

    invoke-virtual {v4, v5, v6, v7}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    goto/16 :goto_2

    :pswitch_15
    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v4

    const/4 v5, 0x5

    move v0, v5

    move v1, v8

    move-object/from16 v2, v18

    invoke-static {v0, v1, v2}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v5

    invoke-virtual {v4, v5, v13}, Lpmsj/work/main/k;->a([La/c/i;B)V

    goto/16 :goto_2

    :pswitch_16
    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v4

    move v0, v8

    move v1, v8

    move-object/from16 v2, v18

    invoke-static {v0, v1, v2}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v5

    invoke-virtual {v4, v5, v6}, Lpmsj/work/main/k;->a([La/c/i;B)V

    goto/16 :goto_2

    :sswitch_5
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    packed-switch v4, :pswitch_data_4

    goto/16 :goto_2

    :pswitch_17
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x80

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v8

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_6
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->P(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_7
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v5

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v9

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v6

    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v10

    const/4 v11, 0x5

    move-object/from16 v0, v18

    move v1, v11

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v11

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v12

    const/16 v13, 0xd8

    invoke-virtual {v12, v13}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ba;

    if-eqz p0, :cond_6

    new-instance v12, Ljava/lang/StringBuilder;

    invoke-direct {v12}, Ljava/lang/StringBuilder;-><init>()V

    const-string v13, "\u51c6\u5907\u767b\u5f55\u6e38\u620f\u670d\u52a1\u5668,nPort="

    invoke-virtual {v12, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v12

    invoke-virtual {v12, v9}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v12

    invoke-virtual {v12}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v12

    invoke-static {v12}, Lpmsj/work/e/ba;->g(Ljava/lang/String;)V

    :cond_6
    if-eqz v9, :cond_3

    sget-object v12, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v12, v12, Lpmsj/work/main/i;->e:La/c/t;

    invoke-virtual {v12}, La/c/t;->a()V

    sget-object v12, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v12, v12, Lpmsj/work/main/i;->e:La/c/t;

    invoke-virtual {v12}, La/c/t;->b()V

    sput v4, La/c/t;->c:I

    sput v5, La/c/t;->d:I

    sget-object v4, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v4, v4, Lpmsj/work/main/i;->f:La/c/t;

    invoke-virtual {v4}, La/c/t;->b()V

    sget-object v4, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v4, v4, Lpmsj/work/main/i;->f:La/c/t;

    invoke-virtual {v4}, La/c/t;->c()V

    sget-boolean v4, Lpmsj/work/main/i;->a:Z

    if-nez v4, :cond_8

    sget-object v4, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v4, v4, Lpmsj/work/main/i;->f:La/c/t;

    new-instance v12, Ljava/lang/StringBuilder;

    invoke-direct {v12}, Ljava/lang/StringBuilder;-><init>()V

    const-string v13, "http://"

    invoke-virtual {v12, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v12

    invoke-virtual {v12, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v12

    const-string v13, ":"

    invoke-virtual {v12, v13}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v12

    invoke-virtual {v12, v9}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v12

    invoke-virtual {v12}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v12

    iput-object v12, v4, La/c/t;->e:Ljava/lang/String;

    :goto_4
    new-instance v4, Ljava/lang/StringBuilder;

    invoke-direct {v4}, Ljava/lang/StringBuilder;-><init>()V

    const-string v12, "\u6e38\u620f\u670d\u52a1\u5668IP"

    invoke-virtual {v4, v12}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    const-string v6, "\u7aef\u53e3"

    invoke-virtual {v4, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4, v9}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v4

    sget-object v6, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v6, v4}, Lpmsj/work/main/i;->a(Ljava/lang/String;)V

    if-eqz p0, :cond_7

    invoke-static {v4}, Lpmsj/work/e/ba;->g(Ljava/lang/String;)V

    :cond_7
    sget-object v4, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v4, v4, Lpmsj/work/main/i;->f:La/c/t;

    iget-object v4, v4, La/c/t;->h:[B

    aput-byte v10, v4, v7

    sget-object v4, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v4, v4, Lpmsj/work/main/i;->f:La/c/t;

    iget-object v4, v4, La/c/t;->h:[B

    aput-byte v11, v4, v8

    sput-boolean v8, Lpmsj/work/main/i;->d:Z

    sget-object v4, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v4, v4, Lpmsj/work/main/i;->f:La/c/t;

    invoke-virtual {v4}, La/c/t;->d()V

    new-instance v4, La/c/r;

    invoke-direct {v4}, La/c/r;-><init>()V

    const/16 v6, 0x41c

    invoke-virtual {v4, v6}, La/c/r;->a(I)V

    sget v6, La/c/t;->c:I

    invoke-virtual {v4, v6}, La/c/r;->d(I)V

    invoke-virtual {v4, v5}, La/c/r;->d(I)V

    sget-object v5, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v4}, La/c/r;->a()[B

    move-result-object v4

    invoke-virtual {v5, v4}, Lpmsj/work/main/i;->b([B)V

    sget-object v4, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v4, v4, Lpmsj/work/main/i;->f:La/c/t;

    iget-byte v5, v4, La/c/t;->b:B

    or-int/lit8 v5, v5, 0x1

    int-to-byte v5, v5

    iput-byte v5, v4, La/c/t;->b:B

    sget-object v4, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v4, v4, Lpmsj/work/main/i;->f:La/c/t;

    invoke-virtual {v4}, La/c/t;->start()V

    goto/16 :goto_2

    :cond_8
    sget-object v4, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    iget-object v4, v4, Lpmsj/work/main/i;->f:La/c/t;

    invoke-static {v6, v9}, Lpmsj/work/a/d;->a(Ljava/lang/String;I)Ljava/lang/String;

    move-result-object v12

    iput-object v12, v4, La/c/t;->e:Ljava/lang/String;

    goto :goto_4

    :sswitch_8
    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v4

    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v5

    const/4 v6, 0x5

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v6

    const/4 v7, 0x6

    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v7

    invoke-static {v4, v7, v5, v6}, Lpmsj/work/main/d;->a(SLjava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    goto/16 :goto_2

    :sswitch_9
    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    const/4 v4, 0x5

    move-object/from16 v0, v18

    move v1, v4

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v4

    sparse-switch v4, :sswitch_data_1

    goto/16 :goto_2

    :sswitch_a
    const/4 v4, 0x6

    invoke-static {v4, v7}, Lpmsj/work/main/e;->a(SI)V

    goto/16 :goto_2

    :sswitch_b
    sget-object v4, Lpmsj/work/main/MyMidlet;->a:Lpmsj/work/main/MyMidlet;

    invoke-virtual {v4}, Lpmsj/work/main/MyMidlet;->a()V

    goto/16 :goto_2

    :sswitch_c
    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v5

    invoke-virtual {v5, v4}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v4

    if-eqz v4, :cond_3

    invoke-virtual {v4}, Lpmsj/work/d/c;->ag()V

    goto/16 :goto_2

    :sswitch_d
    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    const/16 v5, 0x20

    if-ne v4, v5, :cond_9

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v7}, Lpmsj/work/d/n;->i(I)Lpmsj/work/e/ei;

    goto/16 :goto_2

    :cond_9
    const/16 v5, 0xb3

    if-ne v4, v5, :cond_a

    const/16 v4, 0x25a

    :cond_a
    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v12

    const/16 v5, 0x154

    if-ne v4, v5, :cond_b

    const/16 v5, 0x9c4

    if-ne v12, v5, :cond_b

    const/16 v4, 0x265

    :cond_b
    const/16 v5, 0x47

    if-ne v4, v5, :cond_c

    const/16 v5, 0xaf9

    if-ne v12, v5, :cond_c

    const/16 v4, 0x265

    :cond_c
    const/16 v5, 0x18f

    if-ne v4, v5, :cond_d

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/d/n;->i()Lpmsj/work/e/ej;

    goto/16 :goto_2

    :cond_d
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v5

    invoke-virtual {v5, v4}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v11

    packed-switch v4, :pswitch_data_5

    invoke-virtual {v11, v12}, Lpmsj/work/d/c;->y(I)V

    :goto_5
    const/4 v4, 0x6

    move-object/from16 v0, v18

    iget-object v0, v0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    move-object v5, v0

    invoke-virtual {v5}, Ljava/util/Vector;->size()I

    move-result v5

    if-ge v4, v5, :cond_3

    const/4 v4, 0x6

    move-object/from16 v0, v18

    move v1, v4

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v4}, Ljava/lang/String;->length()I

    move-result v5

    if-lez v5, :cond_3

    invoke-virtual {v11, v4}, Lpmsj/work/d/c;->d(Ljava/lang/String;)V

    goto/16 :goto_2

    :pswitch_18
    new-array v6, v13, [Ljava/lang/String;

    const-string v4, "\u5bc4\u5b58"

    aput-object v4, v6, v7

    const-string v4, "\u67e5\u770b"

    aput-object v4, v6, v8

    move-object v0, v11

    check-cast v0, Lpmsj/work/e/cn;

    move-object v4, v0

    sget-object v5, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    move v9, v7

    move v10, v7

    invoke-virtual/range {v4 .. v10}, Lpmsj/work/e/cn;->a(Ljava/util/Vector;[Ljava/lang/String;IZZZ)V

    invoke-virtual {v4, v12}, Lpmsj/work/e/cn;->y(I)V

    goto :goto_5

    :sswitch_e
    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    const/16 v5, 0x182

    if-eq v4, v5, :cond_e

    const/16 v5, 0x181

    if-eq v4, v5, :cond_e

    const/16 v5, 0x18c

    if-eq v4, v5, :cond_e

    const/16 v5, 0x1f5

    if-ne v4, v5, :cond_f

    :cond_e
    const/16 v4, 0x21

    :cond_f
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v5

    invoke-virtual {v5, v4}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x17c

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x17d

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x17e

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    goto/16 :goto_2

    :sswitch_f
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x17c

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x17d

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x17e

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    goto/16 :goto_2

    :sswitch_10
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v5

    invoke-virtual {v4, v5}, Lpmsj/work/b/m;->o(I)Lpmsj/work/b/v;

    move-result-object v4

    if-eqz v4, :cond_3

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v5

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v6

    invoke-virtual {v4, v5, v6}, Lpmsj/work/b/v;->h(II)V

    sget-object v5, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    if-ne v5, v4, :cond_3

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    sget-object v5, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v4, v5}, Lpmsj/work/b/m;->b(Lpmsj/work/b/n;)V

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/main/k;->n()V

    goto/16 :goto_2

    :sswitch_11
    const-string v4, "actionEnterMap"

    invoke-static {v4}, Lpmsj/work/e/ba;->g(Ljava/lang/String;)V

    sget-object v4, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v5

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v6

    invoke-virtual {v4, v5, v6}, Lpmsj/work/b/ab;->h(II)V

    goto/16 :goto_2

    :sswitch_12
    const-string v4, "actionEnterMapOK"

    invoke-static {v4}, Lpmsj/work/e/ba;->g(Ljava/lang/String;)V

    const/16 v4, 0xf

    invoke-static {v4, v7}, Lpmsj/work/main/e;->a(SI)V

    goto/16 :goto_2

    :sswitch_13
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    if-lez v4, :cond_10

    const v5, 0x493df

    if-gt v4, v5, :cond_10

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v5

    invoke-virtual {v5, v4}, Lpmsj/work/b/m;->m(I)V

    goto/16 :goto_2

    :cond_10
    const v5, 0xf4240

    if-lt v4, v5, :cond_3

    const v5, 0x1dcd64ff

    if-gt v4, v5, :cond_3

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v5

    invoke-virtual {v5, v4}, Lpmsj/work/b/m;->p(I)V

    goto/16 :goto_2

    :sswitch_14
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v5

    invoke-virtual {v4, v5}, Lpmsj/work/b/m;->q(I)V

    goto/16 :goto_2

    :sswitch_15
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    invoke-virtual {v4, v5}, Lpmsj/work/b/m;->a(I)V

    goto/16 :goto_2

    :sswitch_16
    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    if-nez v4, :cond_11

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/m;->o()V

    :cond_11
    const-string v4, "actionQueryMapData"

    invoke-static {v4}, Lpmsj/work/e/ba;->g(Ljava/lang/String;)V

    goto/16 :goto_2

    :sswitch_17
    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    if-nez v4, :cond_12

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/m;->c()V

    :cond_12
    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/main/k;->k()V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4, v7}, Lpmsj/work/b/m;->d(I)V

    sget-object v4, La/a/f;->h:La/a/c;

    invoke-virtual {v4}, La/a/c;->b()V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0x2e

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0x12c

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    const-string v4, "actionQueryMapRef"

    invoke-static {v4}, Lpmsj/work/e/ba;->g(Ljava/lang/String;)V

    goto/16 :goto_2

    :sswitch_18
    sput-boolean v8, Lpmsj/work/b/p;->c:Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0x2d

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_2

    :sswitch_19
    sput-boolean v8, Lpmsj/work/main/t;->v:Z

    goto/16 :goto_2

    :sswitch_1a
    sput-boolean v8, Lpmsj/work/main/t;->w:Z

    goto/16 :goto_2

    :sswitch_1b
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/ab;->ag()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/ab;->ah()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v4

    iput v7, v4, Lpmsj/work/b/ab;->T:I

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v4

    new-instance v5, La/b/c;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v6

    iget-byte v6, v6, Lpmsj/work/b/ab;->e:B

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v7

    iget-byte v7, v7, Lpmsj/work/b/ab;->f:B

    invoke-direct {v5, v6, v7}, La/b/c;-><init>(II)V

    iput-object v5, v4, Lpmsj/work/b/ab;->L:La/b/c;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/4 v5, 0x5

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x17e

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x17d

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x17c

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    goto/16 :goto_2

    :sswitch_1c
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v5

    invoke-virtual {v5, v4}, Lpmsj/work/b/m;->o(I)Lpmsj/work/b/v;

    move-result-object v4

    if-eqz v4, :cond_3

    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    invoke-virtual {v4, v5, v7}, Lpmsj/work/b/v;->c(IZ)La/a/d;

    move-result-object v4

    if-eqz v4, :cond_3

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    invoke-virtual {v4, v5}, La/a/d;->d(I)V

    goto/16 :goto_2

    :sswitch_1d
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {}, Lpmsj/work/d/n;->j()Lpmsj/work/e/ei;

    move-result-object v4

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    invoke-virtual {v4, v5}, Lpmsj/work/e/ei;->E(I)V

    goto/16 :goto_2

    :sswitch_1e
    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v5

    invoke-virtual {v5, v4}, Lpmsj/work/b/m;->l(I)Lpmsj/work/b/t;

    move-result-object v5

    if-eqz v5, :cond_3

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v6

    invoke-virtual {v6, v4}, Lpmsj/work/b/m;->e(I)V

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    invoke-static {v5}, Lpmsj/work/main/k;->a(Lpmsj/work/b/n;)V

    goto/16 :goto_2

    :sswitch_1f
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->N(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_20
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->O(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_21
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->M(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_22
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v5

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v9

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v6

    sget-object v10, Lpmsj/work/b/p;->a:Ljava/util/Vector;

    invoke-virtual {v10}, Ljava/util/Vector;->removeAllElements()V

    sget-object v10, Lpmsj/work/b/p;->b:Ljava/util/Vector;

    invoke-virtual {v10}, Ljava/util/Vector;->removeAllElements()V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v10

    const/16 v11, 0x3d

    invoke-virtual {v10, v11}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v10

    invoke-static {}, Lpmsj/work/main/t;->b()Lpmsj/work/main/t;

    move-result-object v11

    iput-boolean v8, v11, Lpmsj/work/main/t;->m:Z

    invoke-virtual {v10, v6}, Lpmsj/work/d/c;->d(Ljava/lang/String;)V

    invoke-static {v7}, Lpmsj/work/b/f;->a(Z)V

    invoke-static {}, Lpmsj/work/b/m;->e()V

    invoke-static {}, Lpmsj/work/main/t;->b()Lpmsj/work/main/t;

    move-result-object v8

    invoke-virtual {v8, v7}, Lpmsj/work/main/t;->d(I)V

    invoke-static {}, Ljava/lang/System;->gc()V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v7

    invoke-virtual {v7, v9, v4, v5, v6}, Lpmsj/work/b/m;->a(IIILjava/lang/String;)V

    const/16 v4, 0x3f2

    const/16 v5, 0xc

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v6

    invoke-virtual {v6}, Lpmsj/work/b/m;->j()I

    move-result v6

    invoke-static {v4, v5, v6}, Lpmsj/work/main/w;->a(ISI)V

    const/16 v4, 0x3f2

    const/16 v5, 0xd

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v6

    invoke-virtual {v6}, Lpmsj/work/b/m;->k()I

    move-result v6

    invoke-static {v4, v5, v6}, Lpmsj/work/main/w;->a(ISI)V

    sget-object v4, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v4}, Lpmsj/work/b/ab;->d()V

    goto/16 :goto_2

    :sswitch_23
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->Q(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_24
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->T(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_25
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/m;->m()Z

    move-result v4

    if-eqz v4, :cond_3

    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v5

    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v6

    const v9, 0xaae61

    if-lt v4, v9, :cond_13

    const v9, 0xc34ff

    if-gt v4, v9, :cond_13

    move v9, v8

    :goto_6
    if-eqz v9, :cond_15

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v8

    invoke-virtual {v8, v4}, Lpmsj/work/b/m;->j(I)Lpmsj/work/b/q;

    move-result-object v4

    if-eqz v4, :cond_3

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v8

    invoke-virtual {v8, v5, v6}, Lpmsj/work/b/m;->b(II)Z

    move-result v8

    if-nez v8, :cond_14

    invoke-static {v14}, La/c/x;->a(I)I

    move-result v8

    packed-switch v8, :pswitch_data_6

    :goto_7
    invoke-virtual {v4, v5, v6, v7}, Lpmsj/work/b/q;->b(IIZ)I

    invoke-virtual {v4}, Lpmsj/work/b/q;->O()V

    goto/16 :goto_2

    :cond_13
    move v9, v7

    goto :goto_6

    :pswitch_19
    invoke-virtual {v4, v5, v6, v7}, Lpmsj/work/b/q;->b(IIZ)I

    goto :goto_7

    :cond_14
    sget-object v4, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v7, Ljava/lang/StringBuilder;

    invoke-direct {v7}, Ljava/lang/StringBuilder;-><init>()V

    const-string v8, "\u660e\u96f7\u602a\u7269\u8d70\u8def:x="

    invoke-virtual {v7, v8}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v7

    invoke-virtual {v7, v5}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v7, ",y="

    invoke-virtual {v5, v7}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, " \u662f\u63a9\u7801"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    goto/16 :goto_2

    :cond_15
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v9

    invoke-virtual {v9, v4}, Lpmsj/work/b/m;->n(I)Lpmsj/work/b/v;

    move-result-object v9

    if-eqz v9, :cond_18

    sget-object v10, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    iget-byte v10, v10, Lpmsj/work/b/ab;->e:B

    sub-int/2addr v10, v5

    invoke-static {v10}, Ljava/lang/Math;->abs(I)I

    move-result v10

    const/16 v11, 0x14

    if-gt v10, v11, :cond_16

    sget-object v10, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    iget-byte v10, v10, Lpmsj/work/b/ab;->f:B

    sub-int/2addr v10, v6

    invoke-static {v10}, Ljava/lang/Math;->abs(I)I

    move-result v10

    const/16 v11, 0x14

    if-le v10, v11, :cond_17

    :cond_16
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v5

    invoke-virtual {v5, v4}, Lpmsj/work/b/m;->p(I)V

    goto/16 :goto_2

    :cond_17
    invoke-virtual {v9}, Lpmsj/work/b/v;->ad()V

    invoke-virtual {v9, v5, v6, v7}, Lpmsj/work/b/v;->b(IIZ)I

    iput-boolean v8, v9, Lpmsj/work/b/v;->H:Z

    goto/16 :goto_2

    :cond_18
    sget-object v7, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    iget-byte v7, v7, Lpmsj/work/b/ab;->e:B

    sub-int v5, v7, v5

    invoke-static {v5}, Ljava/lang/Math;->abs(I)I

    move-result v5

    const/16 v7, 0x14

    if-gt v5, v7, :cond_3

    sget-object v5, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    iget-byte v5, v5, Lpmsj/work/b/ab;->f:B

    sub-int/2addr v5, v6

    invoke-static {v5}, Ljava/lang/Math;->abs(I)I

    move-result v5

    const/16 v6, 0x14

    if-gt v5, v6, :cond_3

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v5

    invoke-virtual {v5}, Lpmsj/work/b/m;->z()Ljava/util/Vector;

    move-result-object v5

    invoke-virtual {v5}, Ljava/util/Vector;->size()I

    move-result v5

    const/16 v6, 0x14

    if-ge v5, v6, :cond_3

    const/16 v5, 0x3f6

    invoke-static {v5, v4}, Lpmsj/work/main/w;->b(II)V

    goto/16 :goto_2

    :sswitch_26
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ai(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_27
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->az(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_28
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->W(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_29
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    packed-switch v4, :pswitch_data_7

    :pswitch_1a
    goto/16 :goto_2

    :pswitch_1b
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4, v5}, Lpmsj/work/b/m;->k(I)V

    goto/16 :goto_2

    :pswitch_1c
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4, v5}, Lpmsj/work/b/m;->j(I)Lpmsj/work/b/q;

    move-result-object v4

    if-eqz v4, :cond_3

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v5

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v6

    const/high16 v7, 0x20000

    invoke-virtual {v4, v6, v7}, Lpmsj/work/b/q;->d(II)Z

    move-result v6

    if-eqz v6, :cond_1a

    const v6, 0x208050

    invoke-virtual {v4, v6, v8}, Lpmsj/work/b/q;->b(IZ)La/a/d;

    :cond_19
    :goto_8
    const/4 v6, 0x6

    invoke-virtual {v4, v6, v5}, Lpmsj/work/b/q;->a(BLjava/lang/Object;)V

    goto/16 :goto_2

    :cond_1a
    invoke-virtual {v5}, La/c/i;->b()I

    move-result v6

    const/high16 v7, 0x20000

    invoke-virtual {v4, v6, v7}, Lpmsj/work/b/q;->e(II)Z

    move-result v6

    if-eqz v6, :cond_19

    const v6, 0x208050

    invoke-virtual {v4, v6}, Lpmsj/work/b/q;->t(I)V

    goto :goto_8

    :sswitch_2a
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->X(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_2b
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->Z(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_2c
    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v5

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v6

    const-string v7, "_"

    invoke-static {v6, v7}, La/c/x;->a(Ljava/lang/String;Ljava/lang/String;)[Ljava/lang/String;

    move-result-object v6

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v7

    const/16 v8, 0x9

    invoke-virtual {v7, v8}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/as;

    const/16 v7, 0x2000

    move-object/from16 v0, p0

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/e/as;->r(I)V

    move-object/from16 v0, p0

    move v1, v4

    move v2, v5

    move-object v3, v6

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/e/as;->a(IS[Ljava/lang/String;)V

    goto/16 :goto_2

    :sswitch_2d
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/4 v5, 0x6

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x4a

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/4 v5, 0x6

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v8

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    goto/16 :goto_2

    :sswitch_2e
    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v4

    sparse-switch v4, :sswitch_data_2

    goto/16 :goto_2

    :sswitch_2f
    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    invoke-static {v4}, Lpmsj/work/b/a;->d(I)Lpmsj/work/b/j;

    move-result-object v5

    if-eqz v5, :cond_3

    invoke-static {v4}, Lpmsj/work/b/a;->e(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/4 v4, 0x5

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0xb

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0xcd

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0x144

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_2

    :sswitch_30
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0x2f

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0x160

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0xb

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_2

    :sswitch_31
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/4 v4, 0x5

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0x12

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_2

    :sswitch_32
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/4 v4, 0x5

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0x12

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_2

    :sswitch_33
    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    invoke-static {v4}, Lpmsj/work/b/a;->b(I)Lpmsj/work/b/j;

    move-result-object v4

    if-eqz v4, :cond_3

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    int-to-short v5, v5

    iput-short v5, v4, Lpmsj/work/b/j;->g:S

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/4 v4, 0x5

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_2

    :sswitch_34
    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v5

    invoke-static {v4, v5}, Lpmsj/work/b/a;->a(ILjava/lang/String;)V

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    invoke-static {v4}, Lpmsj/work/e/b;->D(I)V

    goto/16 :goto_2

    :sswitch_35
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/4 v4, 0x5

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_2

    :sswitch_36
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x165

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_37
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0x144

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_2

    :sswitch_38
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x144

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_39
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x67

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_3a
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x185

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_3b
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v4, 0x185

    invoke-static {v4}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_2

    :sswitch_3c
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x186

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_3d
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ah(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_3e
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    packed-switch v4, :pswitch_data_8

    :pswitch_1d
    goto/16 :goto_2

    :pswitch_1e
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v5

    invoke-virtual {v4, v5}, Lpmsj/work/b/m;->n(I)Lpmsj/work/b/v;

    move-result-object v4

    if-eqz v4, :cond_3

    invoke-virtual {v4}, Lpmsj/work/b/v;->u()I

    move-result v4

    sput v4, Lpmsj/work/b/f;->e:I

    new-instance v5, Ljava/lang/StringBuffer;

    invoke-direct {v5}, Ljava/lang/StringBuffer;-><init>()V

    const-string v4, "*3"

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v4, "*0"

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v4, "\u8bf7\u6c42\u4ea4\u6613,\u662f\u5426\u63a5\u53d7?"

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    invoke-virtual {v5}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v7

    const-string v8, "\u63a5\u53d7"

    const-string v9, "\u62d2\u7edd"

    invoke-virtual/range {v4 .. v9}, Lpmsj/work/d/n;->b(Ljava/lang/String;ILpmsj/work/d/c;Ljava/lang/String;Ljava/lang/String;)Lpmsj/work/e/aa;

    goto/16 :goto_2

    :pswitch_1f
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x10

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v8

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/ab;->ab()Z

    move-result v4

    if-nez v4, :cond_3

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/ab;->ag()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/ab;->ah()V

    goto/16 :goto_2

    :pswitch_20
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x10

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :pswitch_21
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0xb

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x10

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    goto/16 :goto_2

    :sswitch_3f
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    packed-switch v4, :pswitch_data_9

    goto/16 :goto_2

    :pswitch_22
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x132

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_40
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v4

    sparse-switch v4, :sswitch_data_3

    goto/16 :goto_2

    :sswitch_41
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x13d

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x13b

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x13e

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    goto/16 :goto_2

    :sswitch_42
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x132

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/cx;

    if-eqz p0, :cond_1b

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x132

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :cond_1b
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x13e

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_43
    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    sput v4, Lpmsj/work/b/f;->f:I

    new-instance v5, Ljava/lang/StringBuffer;

    invoke-direct {v5}, Ljava/lang/StringBuffer;-><init>()V

    const-string v4, "*3"

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v4, "*0"

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v4, "\u9080\u8bf7\u60a8\u52a0\u5165"

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v4, "*6"

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v4

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v4, "*0"

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v4, "\u662f\u5426\u63a5\u53d7?"

    invoke-virtual {v5, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    invoke-virtual {v5}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v5

    const/16 v6, 0x19

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v7

    const-string v8, "\u63a5\u53d7"

    const-string v9, "\u62d2\u7edd"

    invoke-virtual/range {v4 .. v9}, Lpmsj/work/d/n;->b(Ljava/lang/String;ILpmsj/work/d/c;Ljava/lang/String;Ljava/lang/String;)Lpmsj/work/e/aa;

    goto/16 :goto_2

    :sswitch_44
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    packed-switch v4, :pswitch_data_a

    goto/16 :goto_2

    :pswitch_23
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x13b

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :pswitch_24
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x13d

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_45
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ae(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_46
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->af(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_47
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    packed-switch v4, :pswitch_data_b

    :pswitch_25
    goto/16 :goto_2

    :pswitch_26
    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/main/t;->f()V

    sget-object v4, Lpmsj/work/c/a;->a:Lpmsj/work/c/a;

    if-eqz v4, :cond_1c

    sget-object v4, Lpmsj/work/c/a;->a:Lpmsj/work/c/a;

    invoke-virtual {v4}, Lpmsj/work/c/a;->a()V

    :cond_1c
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x32

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/main/b;->c()V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x14

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x14

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/m;->s()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v4

    invoke-virtual {v4}, Lpmsj/work/b/ab;->am()V

    goto/16 :goto_2

    :pswitch_27
    invoke-static {}, Lpmsj/work/main/t;->f()V

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v4

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v5

    invoke-virtual {v4, v5}, Lpmsj/work/main/b;->a(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x14

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/j;

    if-eqz p0, :cond_3

    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v4

    const/4 v5, 0x5

    move-object/from16 v0, v18

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    const/4 v5, 0x6

    move-object/from16 v0, v18

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v5

    const/4 v9, 0x7

    move-object/from16 v0, v18

    move v1, v9

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-object/from16 v0, p0

    move v1, v4

    move v2, v5

    invoke-virtual {v0, v1, v2}, Lpmsj/work/e/j;->a(SS)V

    const/16 v4, 0x8

    move-object/from16 v0, v18

    move v1, v4

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    if-lez v4, :cond_1d

    move v4, v8

    :goto_9
    move v0, v4

    move-object/from16 v1, p0

    iput-boolean v0, v1, Lpmsj/work/e/j;->a:Z

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    mul-int/lit16 v4, v4, 0x3e8

    move-object/from16 v0, p0

    move v1, v4

    invoke-virtual {v0, v1}, Lpmsj/work/e/j;->D(I)V

    goto/16 :goto_2

    :cond_1d
    move v4, v7

    goto :goto_9

    :pswitch_28
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x14

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/j;

    if-eqz p0, :cond_20

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v5

    invoke-virtual {v5}, Lpmsj/work/main/b;->g()I

    move-result v5

    if-eq v5, v4, :cond_1e

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    const-string v6, "BATTLE_ACTION_SHOW \u4e0b\u53d1\u7684\u56de\u5408\u6570\u548c\u5ba2\u6237\u7aef\u7684\u4e0d\u4e00\u6837\uff0c"

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v6

    invoke-virtual {v6}, Lpmsj/work/main/b;->g()I

    move-result v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v5

    const-string v6, " != "

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5, v4}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-static {v5}, Lpmsj/work/main/b;->a(Ljava/lang/String;)V

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v5

    invoke-virtual {v5, v4}, Lpmsj/work/main/b;->a(I)V

    :cond_1e
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v4

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v5

    iput-byte v5, v4, Lpmsj/work/main/b;->c:B

    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v4

    const/4 v5, 0x5

    move-object/from16 v0, v18

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    const/4 v5, 0x6

    move-object/from16 v0, v18

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v5

    const/4 v6, 0x7

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-object/from16 v0, p0

    move v1, v4

    move v2, v5

    invoke-virtual {v0, v1, v2}, Lpmsj/work/e/j;->a(SS)V

    const/16 v4, 0x8

    move-object/from16 v0, v18

    move v1, v4

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    if-lez v4, :cond_1f

    move v4, v8

    :goto_a
    move v0, v4

    move-object/from16 v1, p0

    iput-boolean v0, v1, Lpmsj/work/e/j;->a:Z

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/e/j;->i()V

    goto/16 :goto_2

    :cond_1f
    move v4, v7

    goto :goto_a

    :cond_20
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    const-string v4, "BATTLE_ACTION_SHOW \u4e0b\u53d1\u7684\u65f6\u5019\u6218\u6597\u5df2\u7ecf\u7ed3\u675f\u4e86"

    invoke-static {v4}, Lpmsj/work/main/b;->a(Ljava/lang/String;)V

    goto/16 :goto_2

    :pswitch_29
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x14

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/j;

    if-eqz p0, :cond_3

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/e/j;->j()V

    invoke-static {}, Lpmsj/work/main/b;->c()V

    goto/16 :goto_2

    :pswitch_2a
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const-string v5, "\u5bf9\u65b9\u4e4b\u524d\u7684\u6218\u6597\u5df2\u7ed3\u675f."

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x191

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v4

    if-eqz v4, :cond_3

    const/16 v4, 0x5ef

    invoke-static {v4, v13}, Lpmsj/work/main/w;->a(IB)V

    goto/16 :goto_2

    :sswitch_48
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->V(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_49
    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v4

    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v9

    move-object/from16 v0, v18

    move v1, v8

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v10

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v11

    move-object/from16 v0, v18

    move v1, v6

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v12

    move-object/from16 v0, v18

    move v1, v14

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v13

    const/4 v5, 0x5

    move-object/from16 v0, v18

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v14

    const/4 v5, 0x6

    move-object/from16 v0, v18

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v15

    const/4 v5, 0x7

    move-object/from16 v0, v18

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v16

    const/16 v5, 0x8

    move-object/from16 v0, v18

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v17

    move-object v8, v4

    invoke-virtual/range {v8 .. v17}, Lpmsj/work/main/k;->a(BIIIIILjava/lang/String;Ljava/lang/String;Ljava/lang/String;)V

    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    goto/16 :goto_2

    :sswitch_4a
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const-string v5, "\u5bf9\u65b9\u7ec4\u961f\uff0c\u786e\u8ba4\u8981PK\u5417\uff1f"

    const/16 v6, 0x1f

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v7

    const-string v8, "\u786e\u5b9a"

    const-string v9, "\u62d2\u7edd"

    invoke-virtual/range {v4 .. v9}, Lpmsj/work/d/n;->b(Ljava/lang/String;ILpmsj/work/d/c;Ljava/lang/String;Ljava/lang/String;)Lpmsj/work/e/aa;

    move-object/from16 v0, v18

    move v1, v13

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    sput v4, Lpmsj/work/main/e;->d:I

    goto/16 :goto_2

    :sswitch_4b
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->U(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_4c
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ag(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_4d
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->aj(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_4e
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ak(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_4f
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->am(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_50
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->al(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_51
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->an(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_52
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->aa(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_53
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ab(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_54
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ac(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_55
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ar(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_56
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ad(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_57
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->a(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_58
    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    packed-switch v4, :pswitch_data_c

    goto/16 :goto_2

    :pswitch_2b
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x60

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v8

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_59
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ap(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_5a
    const-string v4, "processPngQuery"

    invoke-static {v4}, Lpmsj/work/e/ba;->g(Ljava/lang/String;)V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4, v8}, Lpmsj/work/b/m;->d(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x3d

    invoke-virtual {v4, v5}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/bm;

    if-eqz p0, :cond_3

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/e/bm;->i()V

    goto/16 :goto_2

    :sswitch_5b
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ao(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_5c
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->aq(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_5d
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->Y(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_5e
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x13c

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_5f
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v4

    const/16 v5, 0x69

    move-object v0, v4

    move v1, v5

    move-object/from16 v2, v18

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_2

    :sswitch_60
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->S(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_61
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->R(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_62
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->r(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_63
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->s(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_64
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->as(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_65
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->g(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_66
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->o(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_67
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->H(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_68
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->L(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_69
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->at(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_6a
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->au(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_6b
    move-object/from16 v0, v18

    move v1, v7

    invoke-virtual {v0, v1}, Lpmsj/work/main/w;->a(I)B

    goto/16 :goto_2

    :sswitch_6c
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->av(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_6d
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->J(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_6e
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->aw(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_6f
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ax(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_70
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->ay(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_71
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->I(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_72
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->aA(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_73
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->aB(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_74
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->G(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_75
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->F(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_76
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->E(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_77
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->D(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_78
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->B(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_79
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->f(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_7a
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->A(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_7b
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->C(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_7c
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->z(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_7d
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->y(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_7e
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->x(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_7f
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->w(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_80
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->v(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_81
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->u(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_82
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->t(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_83
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->p(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_84
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->q(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_85
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->n(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_86
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->m(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_87
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->l(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_88
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->k(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_89
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->j(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_8a
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->i(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_8b
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->h(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_8c
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->aC(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_8d
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->aD(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_8e
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->aE(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_8f
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->e(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_90
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->d(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_91
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->c(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    :sswitch_92
    invoke-static/range {v18 .. v18}, Lpmsj/work/main/e;->b(Lpmsj/work/main/w;)V

    goto/16 :goto_2

    nop

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_3
        :pswitch_4
        :pswitch_5
        :pswitch_6
        :pswitch_7
    .end packed-switch

    :sswitch_data_0
    .sparse-switch
        0x3eb -> :sswitch_79
        0x3ec -> :sswitch_8
        0x3ed -> :sswitch_25
        0x3ee -> :sswitch_1f
        0x3f0 -> :sswitch_2b
        0x3f1 -> :sswitch_2e
        0x3f2 -> :sswitch_9
        0x3f4 -> :sswitch_64
        0x3f6 -> :sswitch_24
        0x3f7 -> :sswitch_4f
        0x3f9 -> :sswitch_20
        0x3fb -> :sswitch_3d
        0x3ff -> :sswitch_4c
        0x400 -> :sswitch_82
        0x401 -> :sswitch_7a
        0x402 -> :sswitch_4d
        0x406 -> :sswitch_4e
        0x408 -> :sswitch_2c
        0x409 -> :sswitch_65
        0x40e -> :sswitch_26
        0x40f -> :sswitch_45
        0x410 -> :sswitch_47
        0x411 -> :sswitch_48
        0x412 -> :sswitch_4b
        0x418 -> :sswitch_46
        0x419 -> :sswitch_4
        0x41a -> :sswitch_85
        0x41c -> :sswitch_7
        0x41e -> :sswitch_80
        0x41f -> :sswitch_1
        0x420 -> :sswitch_3e
        0x423 -> :sswitch_86
        0x425 -> :sswitch_87
        0x429 -> :sswitch_71
        0x42a -> :sswitch_6d
        0x42b -> :sswitch_81
        0x42c -> :sswitch_89
        0x42d -> :sswitch_88
        0x42f -> :sswitch_78
        0x430 -> :sswitch_7c
        0x431 -> :sswitch_7d
        0x433 -> :sswitch_7e
        0x435 -> :sswitch_62
        0x436 -> :sswitch_63
        0x437 -> :sswitch_89
        0x438 -> :sswitch_2
        0x439 -> :sswitch_75
        0x43a -> :sswitch_7f
        0x43b -> :sswitch_83
        0x43c -> :sswitch_66
        0x43f -> :sswitch_8a
        0x441 -> :sswitch_8c
        0x442 -> :sswitch_8d
        0x443 -> :sswitch_8e
        0x444 -> :sswitch_91
        0x446 -> :sswitch_57
        0x448 -> :sswitch_21
        0x44f -> :sswitch_51
        0x453 -> :sswitch_40
        0x456 -> :sswitch_22
        0x45b -> :sswitch_72
        0x463 -> :sswitch_7b
        0x466 -> :sswitch_23
        0x467 -> :sswitch_52
        0x468 -> :sswitch_8f
        0x469 -> :sswitch_55
        0x46a -> :sswitch_54
        0x46c -> :sswitch_76
        0x46e -> :sswitch_53
        0x46f -> :sswitch_73
        0x470 -> :sswitch_3f
        0x471 -> :sswitch_44
        0x472 -> :sswitch_50
        0x474 -> :sswitch_5e
        0x475 -> :sswitch_60
        0x476 -> :sswitch_61
        0x477 -> :sswitch_77
        0x478 -> :sswitch_69
        0x479 -> :sswitch_6c
        0x481 -> :sswitch_8b
        0x485 -> :sswitch_5
        0x486 -> :sswitch_4a
        0x48f -> :sswitch_0
        0x492 -> :sswitch_74
        0x517 -> :sswitch_58
        0x57b -> :sswitch_56
        0x57f -> :sswitch_68
        0x5dc -> :sswitch_6a
        0x5dd -> :sswitch_59
        0x5de -> :sswitch_5a
        0x5df -> :sswitch_5b
        0x5e0 -> :sswitch_5c
        0x5e1 -> :sswitch_5d
        0x5e2 -> :sswitch_5f
        0x5e5 -> :sswitch_49
        0x5e7 -> :sswitch_6e
        0x5e8 -> :sswitch_6f
        0x5ee -> :sswitch_6b
        0x5ef -> :sswitch_67
        0x5f0 -> :sswitch_84
        0x5f3 -> :sswitch_6
        0x5fd -> :sswitch_3
        0x6c3 -> :sswitch_70
        0x7eb -> :sswitch_27
        0x7ec -> :sswitch_28
        0x7ed -> :sswitch_29
        0x7ee -> :sswitch_2a
        0x7f0 -> :sswitch_2d
        0x834 -> :sswitch_90
        0x139c -> :sswitch_92
    .end sparse-switch

    :pswitch_data_1
    .packed-switch 0x0
        :pswitch_8
        :pswitch_9
    .end packed-switch

    :pswitch_data_2
    .packed-switch 0x0
        :pswitch_b
        :pswitch_c
        :pswitch_d
        :pswitch_10
        :pswitch_e
        :pswitch_11
        :pswitch_12
        :pswitch_a
        :pswitch_f
    .end packed-switch

    :pswitch_data_3
    .packed-switch 0x1
        :pswitch_14
        :pswitch_13
        :pswitch_15
        :pswitch_16
    .end packed-switch

    :pswitch_data_4
    .packed-switch 0x1
        :pswitch_17
    .end packed-switch

    :sswitch_data_1
    .sparse-switch
        0x6 -> :sswitch_a
        0x8 -> :sswitch_10
        0xb -> :sswitch_18
        0xc -> :sswitch_16
        0xd -> :sswitch_17
        0xe -> :sswitch_11
        0x12 -> :sswitch_13
        0x1a -> :sswitch_b
        0x25 -> :sswitch_1d
        0x3d -> :sswitch_15
        0x3f -> :sswitch_1e
        0x45 -> :sswitch_d
        0x46 -> :sswitch_c
        0x47 -> :sswitch_e
        0x48 -> :sswitch_f
        0x60 -> :sswitch_10
        0x66 -> :sswitch_14
        0x69 -> :sswitch_12
        0x115 -> :sswitch_19
        0x116 -> :sswitch_1a
        0x118 -> :sswitch_1b
        0x119 -> :sswitch_1c
    .end sparse-switch

    :pswitch_data_5
    .packed-switch 0x2f
        :pswitch_18
    .end packed-switch

    :pswitch_data_6
    .packed-switch 0x0
        :pswitch_19
    .end packed-switch

    :pswitch_data_7
    .packed-switch 0x0
        :pswitch_1b
        :pswitch_1a
        :pswitch_1c
    .end packed-switch

    :sswitch_data_2
    .sparse-switch
        0x3 -> :sswitch_2f
        0x4 -> :sswitch_30
        0x5 -> :sswitch_31
        0x6 -> :sswitch_32
        0x19 -> :sswitch_33
        0x46 -> :sswitch_36
        0x47 -> :sswitch_36
        0x49 -> :sswitch_38
        0x4a -> :sswitch_3a
        0x4b -> :sswitch_3a
        0x4d -> :sswitch_3a
        0x4e -> :sswitch_3a
        0x52 -> :sswitch_34
        0x53 -> :sswitch_3c
        0x54 -> :sswitch_3c
        0x55 -> :sswitch_3c
        0x56 -> :sswitch_3c
        0x57 -> :sswitch_3c
        0x5a -> :sswitch_37
        0x5b -> :sswitch_37
        0x5c -> :sswitch_3b
        0x5d -> :sswitch_37
        0x5e -> :sswitch_38
        0x5f -> :sswitch_38
        0x60 -> :sswitch_38
        0x61 -> :sswitch_3a
        0x62 -> :sswitch_38
        0x64 -> :sswitch_38
        0x6b -> :sswitch_37
        0x6d -> :sswitch_39
        0x81 -> :sswitch_35
        0x82 -> :sswitch_37
        0x83 -> :sswitch_37
        0x84 -> :sswitch_38
        0x8c -> :sswitch_38
        0x8d -> :sswitch_38
        0x8e -> :sswitch_38
        0x8f -> :sswitch_38
    .end sparse-switch

    :pswitch_data_8
    .packed-switch 0x1
        :pswitch_1e
        :pswitch_1d
        :pswitch_1d
        :pswitch_1d
        :pswitch_1f
        :pswitch_20
        :pswitch_1d
        :pswitch_20
        :pswitch_1d
        :pswitch_20
        :pswitch_21
        :pswitch_21
        :pswitch_1d
        :pswitch_1d
        :pswitch_1d
        :pswitch_1d
        :pswitch_1d
        :pswitch_20
        :pswitch_20
        :pswitch_20
    .end packed-switch

    :pswitch_data_9
    .packed-switch 0x1
        :pswitch_22
    .end packed-switch

    :sswitch_data_3
    .sparse-switch
        0x3 -> :sswitch_41
        0x4 -> :sswitch_41
        0xb -> :sswitch_42
        0x1d -> :sswitch_43
    .end sparse-switch

    :pswitch_data_a
    .packed-switch 0x1
        :pswitch_23
        :pswitch_24
        :pswitch_23
        :pswitch_23
    .end packed-switch

    :pswitch_data_b
    .packed-switch 0x0
        :pswitch_26
        :pswitch_27
        :pswitch_28
        :pswitch_25
        :pswitch_29
        :pswitch_25
        :pswitch_2a
    .end packed-switch

    :pswitch_data_c
    .packed-switch 0x1
        :pswitch_2b
        :pswitch_2b
        :pswitch_2b
    .end packed-switch
.end method

.method private static a(Lpmsj/work/main/w;)V
    .locals 5

    const/4 v1, 0x1

    const/4 v4, 0x0

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x19a

    invoke-virtual {v0, v1, p0, v4}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_1
    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    move v1, v4

    :goto_1
    if-ge v1, v0, :cond_2

    sget-object v2, Lpmsj/work/e/bf;->a:[I

    if-nez v2, :cond_1

    const/4 v2, 0x3

    new-array v2, v2, [I

    sput-object v2, Lpmsj/work/e/bf;->a:[I

    :cond_1
    sget-object v2, Lpmsj/work/e/bf;->a:[I

    add-int/lit8 v3, v1, 0x2

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v3

    aput v3, v2, v1

    add-int/lit8 v1, v1, 0x1

    int-to-byte v1, v1

    goto :goto_1

    :cond_2
    invoke-static {v4, v4}, Lpmsj/work/main/t;->a(ZZ)V

    goto :goto_0

    :pswitch_2
    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    move v1, v4

    :goto_2
    if-ge v1, v0, :cond_4

    sget-object v2, Lpmsj/work/e/bf;->c:[I

    if-nez v2, :cond_3

    new-array v2, v0, [I

    sput-object v2, Lpmsj/work/e/bf;->c:[I

    :cond_3
    sget-object v2, Lpmsj/work/e/bf;->c:[I

    add-int/lit8 v3, v1, 0x2

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v3

    aput v3, v2, v1

    add-int/lit8 v1, v1, 0x1

    int-to-byte v1, v1

    goto :goto_2

    :cond_4
    invoke-static {v4, v4}, Lpmsj/work/main/t;->a(ZZ)V

    goto :goto_0

    :pswitch_3
    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/f;->a(I)Lpmsj/work/b/u;

    move-result-object v0

    if-eqz v0, :cond_0

    iget-object v1, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    if-nez v1, :cond_5

    const/16 v1, 0x446

    const/4 v2, 0x7

    invoke-virtual {v0}, Lpmsj/work/b/u;->u()I

    move-result v0

    invoke-static {v1, v2, v0}, Lpmsj/work/main/w;->a(IBI)V

    goto :goto_0

    :cond_5
    invoke-virtual {v0}, Lpmsj/work/b/u;->a()Lpmsj/work/b/u;

    move-result-object v1

    sput-object v1, Lpmsj/work/b/f;->c:Lpmsj/work/b/u;

    iget-object v0, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    iput-object v0, v1, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    goto :goto_0

    :pswitch_4
    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/f;->a(I)Lpmsj/work/b/u;

    move-result-object v0

    if-eqz v0, :cond_0

    iget-object v1, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    if-eqz v1, :cond_0

    invoke-virtual {v0}, Lpmsj/work/b/u;->a()Lpmsj/work/b/u;

    move-result-object v1

    sput-object v1, Lpmsj/work/b/f;->c:Lpmsj/work/b/u;

    iget-object v0, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    iput-object v0, v1, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    goto/16 :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_4
        :pswitch_0
    .end packed-switch
.end method

.method public static a(SI)V
    .locals 2

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    const/16 v1, 0x3f2

    invoke-virtual {v0, v1}, La/c/r;->a(I)V

    invoke-virtual {v0, p0}, La/c/r;->c(I)V

    invoke-virtual {v0, p1}, La/c/r;->d(I)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method public static a(SLjava/lang/StringBuffer;Ljava/lang/String;Ljava/lang/String;)V
    .locals 3

    const/4 v2, 0x0

    new-instance v0, La/c/r;

    invoke-direct {v0}, La/c/r;-><init>()V

    const/16 v1, 0x3ec

    invoke-virtual {v0, v1}, La/c/r;->a(I)V

    invoke-virtual {v0, v2}, La/c/r;->d(I)V

    invoke-virtual {v0, p0}, La/c/r;->c(I)V

    invoke-virtual {v0, v2}, La/c/r;->c(I)V

    invoke-virtual {v0, v2}, La/c/r;->d(I)V

    invoke-virtual {v0, p3}, La/c/r;->a(Ljava/lang/String;)V

    invoke-virtual {v0, p2}, La/c/r;->a(Ljava/lang/String;)V

    invoke-virtual {p1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, La/c/r;->a(Ljava/lang/String;)V

    sget-object v1, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v0}, La/c/r;->a()[B

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method private static a(La/c/a;I)Z
    .locals 8

    const/4 v7, 0x4

    const/4 v6, 0x0

    sget-object v0, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    aget-object v0, v0, p1

    if-nez v0, :cond_0

    move v0, v6

    :goto_0
    return v0

    :cond_0
    sget-object v0, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    aget-object v1, v0, p1

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v2

    move v3, v6

    :goto_1
    if-ge v3, v2, :cond_3

    invoke-virtual {v1, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-virtual {p0, v6}, La/c/a;->a(I)I

    move-result v4

    invoke-virtual {v0, v6}, La/c/a;->a(I)I

    move-result v5

    if-ne v4, v5, :cond_2

    invoke-virtual {p0, v7}, La/c/a;->a(I)I

    move-result v2

    invoke-virtual {v0, v7}, La/c/a;->a(I)I

    move-result v0

    if-eq v2, v0, :cond_1

    invoke-virtual {v1, p0, v3}, Ljava/util/Vector;->setElementAt(Ljava/lang/Object;I)V

    :cond_1
    const/4 v0, 0x1

    goto :goto_0

    :cond_2
    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_1

    :cond_3
    move v0, v6

    goto :goto_0
.end method

.method private static aA(Lpmsj/work/main/w;)V
    .locals 4

    const/4 v3, 0x0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/b/m;->a(I)V

    new-instance v1, Lpmsj/work/b/n;

    const/4 v2, 0x1

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    invoke-direct {v1, v0, v2, v3, v3}, Lpmsj/work/b/n;-><init>(IIZZ)V

    iput v0, v1, Lpmsj/work/b/n;->j:I

    const/4 v0, 0x2

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    const/4 v2, 0x3

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    invoke-virtual {v1, v0, v2}, Lpmsj/work/b/n;->c(II)V

    const/4 v0, 0x4

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v0

    iput-object v0, v1, Lpmsj/work/b/n;->k:Ljava/lang/String;

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/b/m;->y:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->w()V

    return-void
.end method

.method private static aB(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x195

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    return-void
.end method

.method private static aC(Lpmsj/work/main/w;)V
    .locals 8

    const/4 v7, 0x3

    const/4 v6, 0x1

    const/4 v5, 0x2

    const/4 v4, 0x0

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v7}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/main/k;

    if-eqz v0, :cond_0

    sget-object v2, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    const/16 v3, 0x50

    invoke-virtual {v2, v3}, Lpmsj/work/b/ab;->f(B)I

    move-result v2

    invoke-virtual {v0, v2}, Lpmsj/work/main/k;->b_(I)V

    :cond_0
    packed-switch v1, :pswitch_data_0

    :cond_1
    :goto_0
    return-void

    :pswitch_0
    invoke-static {v4, v4}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    if-lez v0, :cond_4

    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    sub-int/2addr v1, v5

    div-int/2addr v1, v0

    :goto_1
    sget-object v2, Lpmsj/work/b/f;->u:Ljava/util/Vector;

    if-nez v2, :cond_2

    new-instance v2, Ljava/util/Vector;

    invoke-direct {v2}, Ljava/util/Vector;-><init>()V

    sput-object v2, Lpmsj/work/b/f;->u:Ljava/util/Vector;

    :cond_2
    move v2, v4

    :goto_2
    if-ge v2, v0, :cond_1

    mul-int v3, v2, v1

    add-int/lit8 v3, v3, 0x2

    invoke-static {v1, v3, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v3

    sget-object v4, Lpmsj/work/b/f;->u:Ljava/util/Vector;

    invoke-virtual {v4, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_2

    :pswitch_1
    move v2, v4

    :goto_3
    sget-object v0, Lpmsj/work/b/f;->u:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-ge v2, v0, :cond_1

    sget-object v0, Lpmsj/work/b/f;->u:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [La/c/i;

    aget-object v1, v0, v4

    invoke-virtual {v1}, La/c/i;->b()I

    move-result v1

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v3

    if-ne v1, v3, :cond_3

    aget-object v1, v0, v6

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->c(I)I

    move-result v3

    invoke-virtual {v1, v3}, La/c/i;->a(I)V

    aget-object v1, v0, v5

    check-cast v1, La/c/p;

    const/4 v3, 0x4

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v1, v3}, La/c/p;->a(Ljava/lang/String;)V

    sget-object v1, Lpmsj/work/b/f;->u:Ljava/util/Vector;

    invoke-virtual {v1, v0, v2}, Ljava/util/Vector;->setElementAt(Ljava/lang/Object;I)V

    :cond_3
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_3

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x60

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ey;

    invoke-virtual {v0, p0}, Lpmsj/work/e/ey;->b(Lpmsj/work/main/w;)V

    goto :goto_0

    :cond_4
    move v1, v4

    goto :goto_1

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
        :pswitch_2
    .end packed-switch
.end method

.method private static aD(Lpmsj/work/main/w;)V
    .locals 2

    const/4 v0, 0x0

    invoke-static {v0, v0}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x21

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ej;

    if-eqz v0, :cond_0

    const/4 v1, 0x1

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {v0, v1, p0}, Lpmsj/work/e/ej;->a(ILpmsj/work/main/w;)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_1
        :pswitch_0
        :pswitch_1
        :pswitch_1
    .end packed-switch
.end method

.method private static aE(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x1a6

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
    .end packed-switch
.end method

.method private static aa(Lpmsj/work/main/w;)V
    .locals 9

    const/4 v3, 0x2

    const/16 v2, 0x20

    const/4 v6, 0x0

    const/4 v5, 0x1

    invoke-static {v6, v6}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    packed-switch v1, :pswitch_data_0

    :cond_0
    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    new-instance v1, Lpmsj/work/b/u;

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    invoke-direct {v1, v2}, Lpmsj/work/b/u;-><init>(I)V

    move v2, v5

    :goto_1
    if-ge v2, v0, :cond_1

    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v3

    invoke-virtual {v1, v2, v3}, Lpmsj/work/b/u;->a(BLjava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    int-to-byte v2, v2

    goto :goto_1

    :cond_1
    sget-object v0, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v2}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ei;

    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/e/ei;->i()Lpmsj/work/b/u;

    move-result-object v2

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v3

    iput v3, v2, Lpmsj/work/b/u;->j:I

    move v3, v5

    :goto_2
    const/16 v4, 0x9

    if-gt v3, v4, :cond_2

    iget-object v4, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v4, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v4

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/u;->a(BLjava/lang/Object;)V

    add-int/lit8 v3, v3, 0x1

    int-to-byte v3, v3

    goto :goto_2

    :cond_2
    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3}, Ljava/util/Vector;->size()I

    move-result v3

    const/16 v4, 0xa

    sub-int/2addr v3, v4

    move v4, v6

    :goto_3
    if-ge v4, v3, :cond_3

    add-int/lit8 v5, v4, 0x1e

    int-to-byte v5, v5

    iget-object v6, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int/lit8 v7, v4, 0xa

    invoke-virtual {v6, v7}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v6

    invoke-virtual {v2, v5, v6}, Lpmsj/work/b/u;->a(BLjava/lang/Object;)V

    add-int/lit8 v4, v4, 0x1

    int-to-byte v4, v4

    goto :goto_3

    :cond_3
    invoke-virtual {v0}, Lpmsj/work/e/ei;->ag()V

    const/16 v2, 0xf

    if-eq v1, v2, :cond_4

    const/4 v2, 0x4

    if-ne v1, v2, :cond_0

    :cond_4
    invoke-virtual {v0}, Lpmsj/work/e/ei;->p()V

    goto :goto_0

    :pswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v2}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ei;

    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/e/ei;->i()Lpmsj/work/b/u;

    move-result-object v1

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    iput v2, v1, Lpmsj/work/b/u;->j:I

    iget-object v2, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    sub-int/2addr v2, v3

    move v3, v6

    :goto_4
    if-ge v3, v2, :cond_5

    add-int/lit8 v4, v3, 0x1e

    int-to-byte v4, v4

    iget-object v5, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int/lit8 v6, v3, 0x2

    invoke-virtual {v5, v6}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v5

    invoke-virtual {v1, v4, v5}, Lpmsj/work/b/u;->a(BLjava/lang/Object;)V

    add-int/lit8 v3, v3, 0x1

    int-to-byte v3, v3

    goto :goto_4

    :cond_5
    invoke-virtual {v0}, Lpmsj/work/e/ei;->j()V

    invoke-virtual {v0}, Lpmsj/work/e/ei;->ag()V

    goto/16 :goto_0

    :pswitch_4
    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    const/4 v1, 0x0

    iget-object v2, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    sub-int v3, v2, v5

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v3

    sget-object v4, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v4}, Lpmsj/work/b/ab;->u()I

    move-result v4

    if-ne v3, v4, :cond_7

    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-static {v0}, Lpmsj/work/b/f;->a(I)Lpmsj/work/b/u;

    move-result-object v0

    move-object v8, v1

    move-object v1, v0

    move-object v0, v8

    :goto_5
    if-eqz v0, :cond_0

    if-eqz v1, :cond_0

    iget-object v2, v0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    if-eqz v2, :cond_6

    iget-object v2, v0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    invoke-virtual {v2}, Lpmsj/work/b/u;->G()V

    :cond_6
    iput-object v1, v0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    iget-object v1, v0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    invoke-virtual {v1}, Lpmsj/work/b/u;->b()V

    invoke-virtual {v0}, Lpmsj/work/b/v;->ae()V

    goto/16 :goto_0

    :cond_7
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v4

    invoke-virtual {v4, v3}, Lpmsj/work/b/m;->n(I)Lpmsj/work/b/v;

    move-result-object v3

    if-eqz v3, :cond_8

    new-instance v1, Lpmsj/work/b/u;

    invoke-direct {v1, v0}, Lpmsj/work/b/u;-><init>(I)V

    move v0, v5

    :goto_6
    sub-int v4, v2, v5

    if-ge v0, v4, :cond_8

    iget-object v4, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v4, v0}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v4

    invoke-virtual {v1, v0, v4}, Lpmsj/work/b/u;->a(BLjava/lang/Object;)V

    add-int/lit8 v0, v0, 0x1

    int-to-byte v0, v0

    goto :goto_6

    :pswitch_5
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v2}, Lpmsj/work/d/n;->a(I)Z

    goto/16 :goto_0

    :pswitch_6
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/m;->o(I)Lpmsj/work/b/v;

    move-result-object v0

    if-eqz v0, :cond_0

    iget-object v1, v0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    if-eqz v1, :cond_0

    iget-object v1, v0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    invoke-virtual {v1}, Lpmsj/work/b/u;->u()I

    move-result v1

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    if-ne v1, v2, :cond_0

    const/4 v1, 0x3

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    iget-object v2, v0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    iget-object v3, v0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    iget v3, v3, Lpmsj/work/b/u;->B:I

    invoke-virtual {v2, v1, v3}, Lpmsj/work/b/u;->f(II)V

    iget-object v0, v0, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    iput v1, v0, Lpmsj/work/b/u;->B:I

    goto/16 :goto_0

    :cond_8
    move-object v0, v3

    goto :goto_5

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_0
        :pswitch_0
        :pswitch_2
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_3
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_4
        :pswitch_6
        :pswitch_2
        :pswitch_5
    .end packed-switch
.end method

.method private static ab(Lpmsj/work/main/w;)V
    .locals 12

    const/16 v11, 0x2f

    const/16 v10, 0x20

    const/16 v9, 0x69

    const/4 v8, 0x1

    const/4 v7, 0x0

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    invoke-virtual {p0, v8}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    const/4 v3, 0x0

    packed-switch v1, :pswitch_data_0

    :cond_0
    move-object v0, v3

    :goto_0
    if-nez v0, :cond_3

    :cond_1
    :goto_1
    return-void

    :pswitch_0
    invoke-static {v2}, Lpmsj/work/b/f;->a(I)Lpmsj/work/b/u;

    move-result-object v0

    goto :goto_0

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v9}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ck;

    if-eqz v0, :cond_0

    invoke-virtual {v0, v2}, Lpmsj/work/e/ck;->C(I)Lpmsj/work/b/u;

    move-result-object v0

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v9}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ck;

    if-eqz v0, :cond_2

    invoke-virtual {v0}, Lpmsj/work/e/ck;->i()V

    :cond_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v4, 0x8b

    invoke-virtual {v0, v4}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/cl;

    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/e/cl;->i()Lpmsj/work/b/u;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/b/u;->u()I

    move-result v4

    if-ne v4, v2, :cond_0

    goto :goto_0

    :pswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v10}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ei;

    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/e/ei;->i()Lpmsj/work/b/u;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/b/u;->u()I

    move-result v4

    if-ne v4, v2, :cond_0

    goto :goto_0

    :cond_3
    const/4 v2, 0x2

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    move v3, v7

    :goto_2
    if-ge v3, v2, :cond_9

    mul-int/lit8 v4, v3, 0x2

    add-int/lit8 v4, v4, 0x3

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->a(I)B

    move-result v4

    mul-int/lit8 v5, v3, 0x2

    add-int/lit8 v5, v5, 0x4

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v5

    invoke-virtual {v0, v4, v5}, Lpmsj/work/b/u;->a(BLjava/lang/Object;)V

    if-nez v1, :cond_5

    const/16 v6, 0xb

    if-ne v6, v4, :cond_7

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v4

    if-ne v4, v8, :cond_6

    sput-object v0, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    iget-object v4, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    if-nez v4, :cond_4

    :cond_4
    :goto_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v11}, Lpmsj/work/d/n;->h(I)V

    :cond_5
    :goto_4
    add-int/lit8 v3, v3, 0x1

    goto :goto_2

    :cond_6
    sget-object v4, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    if-ne v4, v0, :cond_4

    const/4 v4, 0x0

    sput-object v4, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    goto :goto_3

    :cond_7
    const/16 v5, 0xc

    if-ne v5, v4, :cond_8

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v11}, Lpmsj/work/d/n;->h(I)V

    goto :goto_4

    :cond_8
    const/4 v5, 0x7

    if-ne v5, v4, :cond_5

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v4

    iget-object v4, v4, Lpmsj/work/b/ab;->E:Lpmsj/work/b/u;

    if-ne v0, v4, :cond_5

    const/4 v4, 0x7

    invoke-virtual {v0, v4}, Lpmsj/work/b/u;->f(B)I

    move-result v4

    if-le v4, v8, :cond_5

    const v4, 0x21dfe0

    invoke-virtual {v0, v4, v7, v7}, Lpmsj/work/b/u;->a(IIZ)La/a/d;

    goto :goto_4

    :cond_9
    packed-switch v1, :pswitch_data_1

    goto/16 :goto_1

    :pswitch_4
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v9}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_1

    :pswitch_5
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x8b

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v11}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/cn;

    if-eqz p0, :cond_b

    invoke-virtual {p0}, Lpmsj/work/e/cn;->i()Z

    move-result v0

    if-nez v0, :cond_b

    invoke-virtual {v1, v10}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ei;

    if-eqz v0, :cond_a

    invoke-virtual {v0}, Lpmsj/work/e/ei;->ae()V

    :cond_a
    invoke-virtual {p0, v8}, Lpmsj/work/e/cn;->a(Z)V

    :cond_b
    invoke-virtual {v1, v9}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ck;

    if-eqz p0, :cond_1

    invoke-virtual {p0}, Lpmsj/work/e/ck;->ae()V

    goto/16 :goto_1

    :pswitch_6
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v10}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_1

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
    .end packed-switch

    :pswitch_data_1
    .packed-switch 0x1
        :pswitch_4
        :pswitch_5
        :pswitch_6
    .end packed-switch
.end method

.method private static ac(Lpmsj/work/main/w;)V
    .locals 10

    const/4 v9, 0x3

    const/4 v8, 0x2

    const/16 v6, 0x2f

    const/4 v5, 0x1

    const/4 v7, 0x0

    invoke-static {v7, v7}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    sparse-switch v0, :sswitch_data_0

    :cond_0
    :goto_0
    return-void

    :sswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x20

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ei;

    if-eqz v0, :cond_0

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {v0}, Lpmsj/work/e/ei;->i()Lpmsj/work/b/u;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/u;->u()I

    move-result v0

    if-ne v1, v0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x8c

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/cs;

    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/e/cs;->i()[[La/c/i;

    move-result-object v1

    move v2, v7

    move v3, v8

    :goto_1
    array-length v4, v1

    if-ge v2, v4, :cond_2

    move v4, v3

    move v3, v7

    :goto_2
    aget-object v5, v1, v2

    array-length v5, v5

    if-ge v3, v5, :cond_1

    aget-object v5, v1, v2

    add-int/lit8 v6, v4, 0x1

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v4

    aput-object v4, v5, v3

    add-int/lit8 v3, v3, 0x1

    move v4, v6

    goto :goto_2

    :cond_1
    add-int/lit8 v2, v2, 0x1

    move v3, v4

    goto :goto_1

    :cond_2
    invoke-virtual {v0}, Lpmsj/work/e/cs;->ag()V

    goto :goto_0

    :sswitch_1
    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    sget-object v1, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    invoke-static {v0, v1}, Lpmsj/work/b/f;->a(ILjava/util/Vector;)Lpmsj/work/b/u;

    move-result-object v0

    if-eqz v0, :cond_3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v6}, Lpmsj/work/d/n;->h(I)V

    :cond_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x69

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ck;

    if-eqz p0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/ck;->j()Z

    goto :goto_0

    :sswitch_2
    sget-object v0, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v1

    move v2, v7

    :goto_3
    if-ge v2, v1, :cond_0

    sget-object v0, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/u;

    invoke-virtual {v0}, Lpmsj/work/b/u;->u()I

    move-result v3

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    if-ne v3, v4, :cond_4

    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1, v8}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v1

    invoke-virtual {v0, v9, v1}, Lpmsj/work/b/u;->a(BLjava/lang/Object;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v6}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :cond_4
    add-int/lit8 v0, v2, 0x1

    move v2, v0

    goto :goto_3

    :sswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x30

    invoke-virtual {v0, v1, p0, v7}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_0

    :sswitch_4
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v6}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :sswitch_5
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x30

    invoke-virtual {v0, v1, p0, v7}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_0

    :sswitch_6
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v6}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x20

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/f;->a(I)Lpmsj/work/b/u;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-static {v0}, Lpmsj/work/main/j;->a(Lpmsj/work/b/u;)V

    goto/16 :goto_0

    :sswitch_7
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x203

    invoke-virtual {v0, v1, p0, v7}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_0

    :sswitch_8
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v7}, Lpmsj/work/d/n;->i(I)Lpmsj/work/e/ei;

    move-result-object v0

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    invoke-virtual {v0, v2}, Lpmsj/work/e/ei;->F(I)V

    const/4 v2, 0x0

    sget-object v3, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    invoke-virtual {v3}, Ljava/util/Vector;->size()I

    move-result v3

    move v4, v7

    :goto_4
    if-ge v4, v3, :cond_6

    sget-object v5, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    invoke-virtual {v5, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, Lpmsj/work/b/u;

    invoke-virtual {p0}, Lpmsj/work/b/u;->u()I

    move-result v5

    if-ne v5, v1, :cond_5

    move-object v1, p0

    :goto_5
    const/16 v2, 0x467

    const/16 v3, 0x9

    invoke-virtual {v1}, Lpmsj/work/b/u;->u()I

    move-result v4

    invoke-static {v2, v3, v4}, Lpmsj/work/main/w;->a(IBI)V

    const/16 v2, 0x44f

    const/16 v3, 0xa

    invoke-virtual {v1}, Lpmsj/work/b/u;->u()I

    move-result v4

    invoke-static {v2, v3, v4}, Lpmsj/work/main/w;->a(IBI)V

    invoke-virtual {v1}, Lpmsj/work/b/u;->a()Lpmsj/work/b/u;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/e/ei;->a(Lpmsj/work/b/u;)V

    goto/16 :goto_0

    :cond_5
    add-int/lit8 v4, v4, 0x1

    goto :goto_4

    :sswitch_9
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x168

    invoke-virtual {v0, v1, p0, v7}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_0

    :sswitch_a
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x168

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/cf;

    if-eqz v0, :cond_0

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    if-ne v1, v5, :cond_0

    invoke-virtual {p0, v8}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    const/4 v3, 0x4

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v3

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/e/cf;->a(III)V

    goto/16 :goto_0

    :cond_6
    move-object v1, v2

    goto :goto_5

    nop

    :sswitch_data_0
    .sparse-switch
        0x1 -> :sswitch_1
        0x2 -> :sswitch_3
        0x3 -> :sswitch_4
        0x4 -> :sswitch_5
        0xc -> :sswitch_0
        0xf -> :sswitch_2
        0x10 -> :sswitch_6
        0x32 -> :sswitch_7
        0x33 -> :sswitch_8
        0x34 -> :sswitch_9
        0x35 -> :sswitch_a
    .end sparse-switch
.end method

.method private static ad(Lpmsj/work/main/w;)V
    .locals 10

    const/4 v9, 0x5

    const/4 v6, -0x1

    const/4 v3, 0x2

    const/4 v2, 0x1

    const/4 v8, 0x0

    invoke-static {v8, v8}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v8}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    sparse-switch v0, :sswitch_data_0

    :cond_0
    :goto_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x21

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ej;

    if-eqz p0, :cond_1

    invoke-virtual {p0}, Lpmsj/work/e/ej;->k()V

    :cond_1
    invoke-static {v8, v8}, Lpmsj/work/main/t;->a(ZZ)V

    :cond_2
    :goto_1
    return-void

    :sswitch_0
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/m;->h()I

    move-result v1

    if-ne v0, v1, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v1, 0x6

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/cb;

    invoke-virtual {v0, p0}, Lpmsj/work/e/cb;->b(Lpmsj/work/main/w;)V

    goto :goto_0

    :sswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x4a

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_1

    :sswitch_2
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    const/4 v2, 0x3

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    sget-object v3, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    if-nez v3, :cond_3

    new-array v3, v9, [Ljava/util/Vector;

    sput-object v3, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    :cond_3
    invoke-static {v2}, Lpmsj/work/main/e;->e(I)I

    move-result v2

    if-eq v2, v6, :cond_2

    sget-object v3, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    aget-object v3, v3, v2

    if-nez v3, :cond_4

    sget-object v3, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    new-instance v4, Ljava/util/Vector;

    invoke-direct {v4}, Ljava/util/Vector;-><init>()V

    aput-object v4, v3, v2

    :cond_4
    if-lez v1, :cond_f

    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3}, Ljava/util/Vector;->size()I

    move-result v3

    const/4 v4, 0x4

    sub-int/2addr v3, v4

    div-int/2addr v3, v1

    :goto_2
    sget-object v4, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    aget-object v4, v4, v2

    move v5, v8

    :goto_3
    if-ge v5, v1, :cond_6

    mul-int v6, v5, v3

    add-int/lit8 v6, v6, 0x4

    invoke-virtual {p0, v3, v6}, Lpmsj/work/main/w;->a(II)La/c/a;

    move-result-object v6

    invoke-static {v6, v2}, Lpmsj/work/main/e;->a(La/c/a;I)Z

    move-result v7

    if-nez v7, :cond_5

    invoke-virtual {v4, v6}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_5
    add-int/lit8 v5, v5, 0x1

    goto :goto_3

    :cond_6
    sget-object v1, Lpmsj/work/e/ca;->c:[I

    if-nez v1, :cond_7

    new-array v1, v9, [I

    sput-object v1, Lpmsj/work/e/ca;->c:[I

    :cond_7
    sget-object v1, Lpmsj/work/e/ca;->c:[I

    add-int/lit8 v0, v0, 0x1

    aput v0, v1, v2

    goto/16 :goto_0

    :sswitch_3
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    const/16 v1, 0x8

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    invoke-static {v1}, Lpmsj/work/main/e;->e(I)I

    move-result v1

    sget-object v2, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    if-eqz v2, :cond_0

    sget-object v2, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    aget-object v2, v2, v1

    if-eqz v2, :cond_0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    invoke-static {v2, v1}, Lpmsj/work/main/e;->b(II)I

    move-result v2

    if-eq v6, v2, :cond_0

    sget-object v3, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    aget-object v3, v3, v1

    invoke-virtual {v3, v2}, Ljava/util/Vector;->removeElementAt(I)V

    sget-object v4, Lpmsj/work/e/ca;->c:[I

    if-nez v4, :cond_8

    new-array v4, v9, [I

    sput-object v4, Lpmsj/work/e/ca;->c:[I

    :cond_8
    sget-object v4, Lpmsj/work/e/ca;->c:[I

    add-int/lit8 v0, v0, 0x1

    aput v0, v4, v1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x21

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ej;

    const/4 v1, 0x3

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    if-nez v1, :cond_9

    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/e/ej;->j()V

    goto/16 :goto_0

    :cond_9
    new-instance v1, La/c/a;

    invoke-direct {v1, v9}, La/c/a;-><init>(I)V

    iget-object v4, v1, La/c/a;->a:[La/c/i;

    move v5, v8

    :goto_4
    if-ge v5, v9, :cond_a

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int/lit8 v6, v5, 0x3

    invoke-virtual {v0, v6}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    aput-object v0, v4, v5

    add-int/lit8 v0, v5, 0x1

    move v5, v0

    goto :goto_4

    :cond_a
    invoke-virtual {v3, v1, v2}, Ljava/util/Vector;->insertElementAt(Ljava/lang/Object;I)V

    goto/16 :goto_0

    :sswitch_4
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    sget-object v2, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    if-nez v2, :cond_b

    new-instance v2, Ljava/util/Vector;

    invoke-direct {v2}, Ljava/util/Vector;-><init>()V

    sput-object v2, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    :cond_b
    if-lez v1, :cond_e

    iget-object v2, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    const/4 v3, 0x3

    sub-int/2addr v2, v3

    div-int/2addr v2, v1

    :goto_5
    move v3, v8

    :goto_6
    if-ge v3, v1, :cond_d

    mul-int v4, v3, v2

    add-int/lit8 v4, v4, 0x3

    invoke-virtual {p0, v2, v4}, Lpmsj/work/main/w;->a(II)La/c/a;

    move-result-object v4

    invoke-static {v4}, Lpmsj/work/main/e;->a(La/c/a;)I

    move-result v5

    if-ne v6, v5, :cond_c

    sget-object v5, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    invoke-virtual {v5, v4}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    :cond_c
    add-int/lit8 v3, v3, 0x1

    goto :goto_6

    :cond_d
    sput v0, Lpmsj/work/e/en;->a:I

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x198

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/en;

    if-eqz p0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/en;->ag()V

    goto/16 :goto_0

    :sswitch_5
    sget-object v0, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    if-eqz v0, :cond_0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/main/e;->f(I)I

    move-result v0

    if-eq v6, v0, :cond_0

    sget-object v1, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    iget-object v0, v0, La/c/a;->a:[La/c/i;

    aget-object v0, v0, v3

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    invoke-virtual {v0, v1}, La/c/i;->a(I)V

    goto/16 :goto_0

    :sswitch_6
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    sget-object v1, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    if-eqz v1, :cond_0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-static {v1}, Lpmsj/work/main/e;->f(I)I

    move-result v1

    if-eq v6, v1, :cond_0

    sget-object v2, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    invoke-virtual {v2, v1}, Ljava/util/Vector;->removeElementAt(I)V

    sput v0, Lpmsj/work/e/en;->a:I

    goto/16 :goto_0

    :cond_e
    move v2, v8

    goto :goto_5

    :cond_f
    move v3, v8

    goto/16 :goto_2

    :sswitch_data_0
    .sparse-switch
        0x2 -> :sswitch_2
        0x3 -> :sswitch_2
        0x6 -> :sswitch_2
        0x7 -> :sswitch_3
        0x9 -> :sswitch_2
        0xc -> :sswitch_1
        0xd -> :sswitch_1
        0xe -> :sswitch_1
        0xf -> :sswitch_1
        0x14 -> :sswitch_0
        0x16 -> :sswitch_1
        0x17 -> :sswitch_1
        0x28 -> :sswitch_2
        0x32 -> :sswitch_4
        0x33 -> :sswitch_5
        0x34 -> :sswitch_4
        0x35 -> :sswitch_6
    .end sparse-switch
.end method

.method private static ae(Lpmsj/work/main/w;)V
    .locals 8

    const/16 v7, 0x166

    const/4 v6, 0x2

    const/4 v3, 0x0

    const/4 v5, 0x1

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/main/b;->g:Lpmsj/work/a/l;

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/a/l;->b(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/h;

    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/b/h;->a()I

    move-result v1

    if-ne v5, v1, :cond_1

    const/16 v1, 0x16

    :goto_1
    move v2, v6

    :goto_2
    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3}, Ljava/util/Vector;->size()I

    move-result v3

    if-ge v2, v3, :cond_2

    add-int v3, v1, v2

    sub-int/2addr v3, v6

    int-to-byte v3, v3

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v4

    invoke-virtual {v0, v3, v4}, Lpmsj/work/b/h;->a(BLjava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_2

    :cond_1
    const/16 v1, 0xe

    goto :goto_1

    :cond_2
    sput-boolean v5, Lpmsj/work/b/b;->j:Z

    goto :goto_0

    :pswitch_1
    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    sub-int v1, v0, v5

    new-array v2, v1, [La/c/i;

    :goto_3
    if-ge v3, v1, :cond_3

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int/lit8 v4, v3, 0x1

    invoke-virtual {v0, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    aput-object v0, v2, v3

    add-int/lit8 v0, v3, 0x1

    int-to-byte v0, v0

    move v3, v0

    goto :goto_3

    :cond_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v7}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/di;

    if-eqz p0, :cond_0

    invoke-virtual {p0, v2}, Lpmsj/work/e/di;->a([La/c/i;)V

    invoke-virtual {p0}, Lpmsj/work/e/di;->ag()V

    goto :goto_0

    :pswitch_2
    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    sub-int v1, v0, v5

    new-array v2, v1, [La/c/i;

    :goto_4
    if-ge v3, v1, :cond_4

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    add-int/lit8 v4, v3, 0x1

    invoke-virtual {v0, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/i;

    aput-object v0, v2, v3

    add-int/lit8 v0, v3, 0x1

    int-to-byte v0, v0

    move v3, v0

    goto :goto_4

    :cond_4
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v7}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/di;

    if-eqz p0, :cond_0

    invoke-virtual {p0, v2}, Lpmsj/work/e/di;->a([La/c/i;)V

    invoke-virtual {p0}, Lpmsj/work/e/di;->ag()V

    goto/16 :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
        :pswitch_2
    .end packed-switch
.end method

.method private static af(Lpmsj/work/main/w;)V
    .locals 11

    const/4 v9, 0x2

    const/4 v8, 0x5

    const/4 v7, 0x1

    const/4 v6, 0x3

    const/4 v5, 0x0

    const/4 v0, 0x7

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    const/16 v1, 0x9

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    const/4 v2, 0x0

    packed-switch v0, :pswitch_data_0

    :pswitch_0
    move-object v0, v2

    :goto_0
    if-nez v0, :cond_0

    :goto_1
    return-void

    :pswitch_1
    const/4 v0, 0x6

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    div-int/lit8 v2, v2, 0xa

    invoke-static {v2}, Lpmsj/work/b/h;->f(I)I

    move-result v2

    invoke-virtual {p0, v8}, Lpmsj/work/main/w;->d(I)I

    move-result v3

    if-ne v6, v3, :cond_9

    const v0, 0x186a0

    move v2, v7

    :goto_2
    new-instance v3, Lpmsj/work/b/h;

    const/16 v4, 0x15

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->b(I)S

    move-result v4

    invoke-direct {v3, v1, v2, v0, v4}, Lpmsj/work/b/h;-><init>(IBII)V

    move-object v0, v3

    goto :goto_0

    :pswitch_2
    new-instance v0, Lpmsj/work/b/h;

    const/4 v2, 0x6

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v3

    add-int/lit8 v3, v3, 0x1

    invoke-direct {v0, v1, v2, v3, v5}, Lpmsj/work/b/h;-><init>(IBII)V

    goto :goto_0

    :pswitch_3
    new-instance v0, Lpmsj/work/b/h;

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    add-int/lit8 v2, v2, 0x1

    invoke-direct {v0, v1, v8, v2, v5}, Lpmsj/work/b/h;-><init>(IBII)V

    goto :goto_0

    :cond_0
    move v2, v5

    :goto_3
    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3}, Ljava/util/Vector;->size()I

    move-result v3

    if-ge v2, v3, :cond_1

    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v3

    invoke-virtual {v0, v2, v3}, Lpmsj/work/b/h;->a(BLjava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    int-to-byte v2, v2

    goto :goto_3

    :cond_1
    const/high16 v2, 0x800000

    invoke-virtual {v0, v2}, Lpmsj/work/b/h;->a(I)Z

    move-result v2

    if-eqz v2, :cond_2

    const v2, 0x9c40

    invoke-virtual {v0, v2, v7}, Lpmsj/work/b/h;->c(IZ)La/a/d;

    :cond_2
    invoke-virtual {v0}, Lpmsj/work/b/h;->a()I

    move-result v2

    if-ne v7, v2, :cond_5

    invoke-virtual {v0}, Lpmsj/work/b/h;->r()V

    :goto_4
    invoke-virtual {v0}, Lpmsj/work/b/h;->d()Z

    move-result v2

    if-eqz v2, :cond_3

    const/16 v2, 0x63

    invoke-virtual {v0, v2}, Lpmsj/work/b/h;->b(B)V

    :cond_3
    invoke-virtual {v0, v8}, Lpmsj/work/b/h;->f(B)I

    move-result v2

    if-ne v6, v2, :cond_6

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v2

    iget-object v2, v2, Lpmsj/work/main/b;->h:Lpmsj/work/a/l;

    if-nez v2, :cond_4

    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v2

    new-instance v3, Lpmsj/work/a/l;

    invoke-direct {v3}, Lpmsj/work/a/l;-><init>()V

    iput-object v3, v2, Lpmsj/work/main/b;->h:Lpmsj/work/a/l;

    :cond_4
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v2

    iget-object v2, v2, Lpmsj/work/main/b;->h:Lpmsj/work/a/l;

    invoke-virtual {v2, v1, v0}, Lpmsj/work/a/l;->a(ILjava/lang/Object;)Ljava/lang/Object;

    goto/16 :goto_1

    :cond_5
    const/16 v2, 0xd

    invoke-virtual {v0, v2}, Lpmsj/work/b/h;->f(B)I

    move-result v2

    invoke-virtual {v0, v2}, Lpmsj/work/b/h;->d(I)V

    invoke-virtual {v0, v9}, Lpmsj/work/b/h;->f(B)I

    move-result v2

    invoke-virtual {v0, v2}, Lpmsj/work/b/h;->e(I)V

    goto :goto_4

    :cond_6
    invoke-virtual {v0}, Lpmsj/work/b/h;->u()I

    move-result v2

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v3

    invoke-virtual {v3}, Lpmsj/work/b/ab;->u()I

    move-result v3

    if-ne v2, v3, :cond_8

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    const/16 v3, 0x28

    invoke-virtual {v0, v6}, Lpmsj/work/b/h;->f(B)I

    move-result v4

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/ab;->a(BI)V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    const/16 v3, 0x29

    const/16 v4, 0xb

    invoke-virtual {v0, v4}, Lpmsj/work/b/h;->f(B)I

    move-result v4

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/ab;->a(BI)V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    const/16 v3, 0x2a

    const/16 v4, 0xa

    invoke-virtual {v0, v4}, Lpmsj/work/b/h;->f(B)I

    move-result v4

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/ab;->a(BI)V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    const/16 v3, 0x2b

    const/16 v4, 0xc

    invoke-virtual {v0, v4}, Lpmsj/work/b/h;->f(B)I

    move-result v4

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/ab;->a(BI)V

    :cond_7
    :goto_5
    invoke-static {}, Lpmsj/work/main/b;->b()Lpmsj/work/main/b;

    move-result-object v2

    iget-object v2, v2, Lpmsj/work/main/b;->g:Lpmsj/work/a/l;

    invoke-virtual {v2, v1, v0}, Lpmsj/work/a/l;->a(ILjava/lang/Object;)Ljava/lang/Object;

    goto/16 :goto_1

    :cond_8
    sget-object v2, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    if-eqz v2, :cond_7

    sget-object v2, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    invoke-virtual {v2}, Lpmsj/work/b/u;->u()I

    move-result v2

    invoke-virtual {v0}, Lpmsj/work/b/h;->u()I

    move-result v3

    if-ne v2, v3, :cond_7

    sget-object v2, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v3, 0x26

    invoke-virtual {v0, v6}, Lpmsj/work/b/h;->f(B)I

    move-result v4

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/u;->a(BI)V

    sget-object v2, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v3, 0x27

    const/16 v4, 0xb

    invoke-virtual {v0, v4}, Lpmsj/work/b/h;->f(B)I

    move-result v4

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/u;->a(BI)V

    sget-object v2, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v3, 0x28

    const/16 v4, 0xa

    invoke-virtual {v0, v4}, Lpmsj/work/b/h;->f(B)I

    move-result v4

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/u;->a(BI)V

    sget-object v2, Lpmsj/work/b/f;->b:Lpmsj/work/b/u;

    const/16 v3, 0x29

    const/16 v4, 0xc

    invoke-virtual {v0, v4}, Lpmsj/work/b/h;->f(B)I

    move-result v4

    invoke-virtual {v2, v3, v4}, Lpmsj/work/b/u;->a(BI)V

    goto :goto_5

    :cond_9
    move v10, v2

    move v2, v0

    move v0, v10

    goto/16 :goto_2

    nop

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_2
        :pswitch_0
        :pswitch_3
    .end packed-switch
.end method

.method private static ag(Lpmsj/work/main/w;)V
    .locals 8

    const/4 v3, 0x5

    const/16 v7, 0x3ff

    const/16 v2, 0x5c

    const/4 v1, 0x0

    const/4 v6, 0x1

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    sparse-switch v0, :sswitch_data_0

    :cond_0
    :goto_0
    return-void

    :sswitch_0
    invoke-static {v3, v6, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v0

    aget-object v1, v0, v1

    invoke-virtual {v1}, La/c/i;->b()I

    move-result v1

    sget-boolean v2, Lpmsj/work/b/aa;->e:Z

    if-eqz v2, :cond_1

    const/16 v0, 0xa

    invoke-static {v7, v0, v1}, Lpmsj/work/main/w;->a(ISI)V

    goto :goto_0

    :cond_1
    invoke-static {v0}, Lpmsj/work/b/aa;->b([La/c/i;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x51

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    goto :goto_0

    :sswitch_1
    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    sget-boolean v0, Lpmsj/work/b/aa;->f:Z

    if-eqz v0, :cond_2

    invoke-static {}, Lpmsj/work/main/w;->a()Lpmsj/work/main/w;

    invoke-static {v7, v3, v1}, Lpmsj/work/main/w;->a(ISI)V

    goto :goto_0

    :cond_2
    sget-object v0, Lpmsj/work/b/aa;->c:La/c/e;

    invoke-virtual {v0, v1}, La/c/e;->b(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Ljava/lang/Long;

    if-eqz v0, :cond_3

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v2

    invoke-virtual {v0}, Ljava/lang/Long;->longValue()J

    move-result-wide v4

    sub-long/2addr v2, v4

    const-wide/32 v4, 0xea60

    cmp-long v0, v2, v4

    if-gez v0, :cond_3

    invoke-static {}, Lpmsj/work/main/w;->a()Lpmsj/work/main/w;

    const/16 v0, 0x26

    invoke-static {v7, v0, v1}, Lpmsj/work/main/w;->a(ISI)V

    goto :goto_0

    :cond_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x53

    invoke-virtual {v0, v1, p0, v6}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :sswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x5d

    invoke-virtual {v0, v1, p0, v6}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :sswitch_3
    invoke-static {}, Lpmsj/work/b/aa;->i()V

    goto :goto_0

    :sswitch_4
    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/aa;->d(I)V

    goto :goto_0

    :sswitch_5
    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->u()I

    move-result v1

    if-ne v1, v0, :cond_4

    invoke-static {}, Lpmsj/work/b/aa;->i()V

    goto/16 :goto_0

    :cond_4
    invoke-static {v0}, Lpmsj/work/b/aa;->a(I)Z

    move-result v1

    if-eqz v1, :cond_6

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v2}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/b/m;->n(I)Lpmsj/work/b/v;

    move-result-object v0

    if-eqz v0, :cond_6

    iget-boolean v1, v0, Lpmsj/work/b/v;->y:Z

    if-eqz v1, :cond_5

    invoke-virtual {v0}, Lpmsj/work/b/v;->I()V

    :cond_5
    invoke-virtual {v0}, Lpmsj/work/b/v;->ad()V

    invoke-virtual {v0}, Lpmsj/work/b/v;->ae()V

    :cond_6
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->Z()Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/b/aa;->h()V

    goto/16 :goto_0

    :sswitch_6
    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-static {v0, v1}, Lpmsj/work/b/aa;->a(IZ)V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->u()I

    move-result v0

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    if-ne v0, v1, :cond_7

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->ag()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->ah()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->d()V

    :cond_7
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->Z()Z

    move-result v0

    if-eqz v0, :cond_8

    invoke-static {}, Lpmsj/work/b/aa;->h()V

    :cond_8
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v2}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :sswitch_7
    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-static {v0, v6}, Lpmsj/work/b/aa;->a(IZ)V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->Z()Z

    move-result v0

    if-eqz v0, :cond_9

    invoke-static {}, Lpmsj/work/b/aa;->h()V

    :cond_9
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/m;->o(I)Lpmsj/work/b/v;

    move-result-object v0

    if-eqz v0, :cond_b

    iget-boolean v1, v0, Lpmsj/work/b/v;->y:Z

    if-eqz v1, :cond_a

    invoke-virtual {v0}, Lpmsj/work/b/v;->I()V

    :cond_a
    invoke-virtual {v0}, Lpmsj/work/b/v;->ad()V

    invoke-virtual {v0}, Lpmsj/work/b/v;->ae()V

    :cond_b
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v2}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :sswitch_8
    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/aa;->g(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x51

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    nop

    :sswitch_data_0
    .sparse-switch
        0x1 -> :sswitch_5
        0x2 -> :sswitch_1
        0x6 -> :sswitch_0
        0xb -> :sswitch_3
        0xc -> :sswitch_5
        0x11 -> :sswitch_6
        0x12 -> :sswitch_7
        0x14 -> :sswitch_4
        0x16 -> :sswitch_8
        0x32 -> :sswitch_2
    .end sparse-switch
.end method

.method private static ah(Lpmsj/work/main/w;)V
    .locals 12

    const/4 v11, 0x3

    const/4 v4, 0x0

    const/4 v2, 0x2

    const/4 v10, 0x0

    const/4 v9, 0x1

    invoke-static {v10, v10}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v10}, Lpmsj/work/main/w;->a(I)B

    move-result v3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x25e

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ei;

    if-eqz v0, :cond_d

    invoke-virtual {v0, v9}, Lpmsj/work/e/ei;->G(I)Lpmsj/work/d/c;

    move-result-object v1

    check-cast v1, Lpmsj/work/e/an;

    invoke-virtual {v0, v2}, Lpmsj/work/e/ei;->G(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ae;

    move-object v6, v0

    move-object v7, v1

    :goto_0
    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    const/16 v1, 0x1c

    if-ne v1, v3, :cond_0

    sget-object v1, Lpmsj/work/b/f;->h:Ljava/util/Vector;

    if-nez v1, :cond_0

    new-instance v1, Ljava/util/Vector;

    invoke-direct {v1}, Ljava/util/Vector;-><init>()V

    sput-object v1, Lpmsj/work/b/f;->h:Ljava/util/Vector;

    :cond_0
    packed-switch v3, :pswitch_data_0

    :cond_1
    :goto_1
    :pswitch_0
    if-eqz v7, :cond_2

    invoke-virtual {v7}, Lpmsj/work/e/an;->i()V

    :cond_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x262

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/an;

    if-eqz p0, :cond_3

    invoke-virtual {p0}, Lpmsj/work/e/an;->i()V

    :cond_3
    if-eqz v6, :cond_4

    invoke-virtual {v6}, Lpmsj/work/e/ae;->i()V

    :cond_4
    return-void

    :pswitch_1
    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    move v1, v10

    :goto_2
    if-ge v1, v0, :cond_1

    const/4 v2, 0x5

    mul-int/lit8 v4, v1, 0x5

    add-int/lit8 v4, v4, 0x2

    invoke-static {v2, v4, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v2

    const/16 v4, 0x1c

    if-ne v3, v4, :cond_6

    sget-object v4, Lpmsj/work/b/f;->h:Ljava/util/Vector;

    invoke-virtual {v4, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    aget-object v2, v2, v9

    invoke-virtual {v2}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v2

    invoke-static {v2}, Lpmsj/work/b/f;->b(Ljava/lang/String;)Z

    :cond_5
    :goto_3
    add-int/lit8 v1, v1, 0x1

    int-to-byte v1, v1

    goto :goto_2

    :cond_6
    const/16 v4, 0xf

    if-ne v3, v4, :cond_5

    sget-object v4, Lpmsj/work/b/f;->g:Ljava/util/Vector;

    invoke-virtual {v4, v2}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_3

    :pswitch_2
    const/16 v0, 0xc

    if-ne v3, v0, :cond_7

    sget-object v0, Lpmsj/work/b/f;->g:Ljava/util/Vector;

    move-object v1, v0

    :goto_4
    if-eqz v1, :cond_1

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v3

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    move v5, v10

    :goto_5
    if-ge v5, v3, :cond_1

    invoke-virtual {v1, v5}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, [La/c/i;

    aget-object v8, v0, v10

    invoke-virtual {v8}, La/c/i;->b()I

    move-result v8

    if-ne v8, v4, :cond_8

    aget-object v1, v0, v2

    invoke-virtual {v1, v9}, La/c/i;->a(I)V

    aget-object v0, v0, v11

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {v0, v1}, La/c/i;->a(I)V

    goto :goto_1

    :cond_7
    const/16 v0, 0x10

    if-ne v3, v0, :cond_c

    sget-object v0, Lpmsj/work/b/f;->h:Ljava/util/Vector;

    move-object v1, v0

    goto :goto_4

    :cond_8
    add-int/lit8 v0, v5, 0x1

    move v5, v0

    goto :goto_5

    :pswitch_3
    const/16 v0, 0xd

    if-ne v3, v0, :cond_9

    sget-object v0, Lpmsj/work/b/f;->g:Ljava/util/Vector;

    :goto_6
    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v1

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->c(I)I

    move-result v3

    move v4, v10

    :goto_7
    if-ge v4, v1, :cond_1

    invoke-virtual {v0, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object p0

    check-cast p0, [La/c/i;

    aget-object v5, p0, v10

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v5

    if-ne v5, v3, :cond_a

    aget-object v0, p0, v2

    invoke-virtual {v0, v10}, La/c/i;->a(I)V

    goto/16 :goto_1

    :cond_9
    const/16 v0, 0x11

    if-ne v3, v0, :cond_b

    sget-object v0, Lpmsj/work/b/f;->h:Ljava/util/Vector;

    goto :goto_6

    :cond_a
    add-int/lit8 v4, v4, 0x1

    goto :goto_7

    :pswitch_4
    sub-int/2addr v0, v9

    new-array v0, v0, [Ljava/lang/String;

    sput-object v0, Lpmsj/work/main/k;->a:[Ljava/lang/String;

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-static {v1}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

    move-result-object v1

    aput-object v1, v0, v10

    sget-object v0, Lpmsj/work/main/k;->a:[Ljava/lang/String;

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v1

    aput-object v1, v0, v9

    sget-object v0, Lpmsj/work/main/k;->a:[Ljava/lang/String;

    invoke-virtual {p0, v11}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    invoke-static {v1}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

    move-result-object v1

    aput-object v1, v0, v2

    sget-object v0, Lpmsj/work/main/k;->a:[Ljava/lang/String;

    const/4 v1, 0x4

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-static {v1}, Ljava/lang/Integer;->toString(I)Ljava/lang/String;

    move-result-object v1

    aput-object v1, v0, v11

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    const-string v3, "\u8bf7\u6c42\u52a0\u60a8\u4e3a\u597d\u53cb\uff0c\u662f\u5426\u786e\u5b9a\uff1f"

    invoke-virtual {v1, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v3

    const-string v4, "\u63a5\u53d7"

    const-string v5, "\u62d2\u7edd"

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/d/n;->b(Ljava/lang/String;ILpmsj/work/d/c;Ljava/lang/String;Ljava/lang/String;)Lpmsj/work/e/aa;

    goto/16 :goto_1

    :pswitch_5
    sget-object v0, Lpmsj/work/b/f;->g:Ljava/util/Vector;

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-static {v0, v1}, Lpmsj/work/b/f;->a(Ljava/util/Vector;I)V

    goto/16 :goto_1

    :pswitch_6
    sget-object v0, Lpmsj/work/b/f;->h:Ljava/util/Vector;

    if-eqz v0, :cond_1

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    sget-object v1, Lpmsj/work/b/f;->h:Ljava/util/Vector;

    invoke-static {v1, v0}, Lpmsj/work/b/f;->a(Ljava/util/Vector;I)V

    goto/16 :goto_1

    :cond_b
    move-object v0, v4

    goto/16 :goto_6

    :cond_c
    move-object v1, v4

    goto/16 :goto_4

    :cond_d
    move-object v6, v4

    move-object v7, v4

    goto/16 :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0xa
        :pswitch_4
        :pswitch_0
        :pswitch_2
        :pswitch_3
        :pswitch_5
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_6
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_1
    .end packed-switch
.end method

.method private static ai(Lpmsj/work/main/w;)V
    .locals 7

    const/4 v6, 0x0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->m()Z

    move-result v0

    if-nez v0, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/m;->o(I)Lpmsj/work/b/v;

    move-result-object v0

    if-eqz v0, :cond_0

    const/4 v1, 0x1

    iput-boolean v1, v0, Lpmsj/work/b/v;->H:Z

    const/4 v1, 0x5

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    move v2, v6

    move-object v3, v0

    :goto_1
    if-ge v2, v1, :cond_3

    add-int/lit8 v4, v2, 0x6

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v5

    invoke-virtual {v5, v4}, Lpmsj/work/b/m;->o(I)Lpmsj/work/b/v;

    move-result-object v4

    if-eqz v4, :cond_2

    iput-boolean v6, v4, Lpmsj/work/b/v;->H:Z

    invoke-virtual {v4}, Lpmsj/work/b/v;->E()V

    invoke-virtual {v3, v4}, Lpmsj/work/b/v;->a(Lpmsj/work/b/n;)V

    move-object v3, v4

    :cond_2
    add-int/lit8 v2, v2, 0x1

    goto :goto_1

    :cond_3
    const/4 v1, 0x0

    invoke-virtual {v3, v1}, Lpmsj/work/b/v;->a(Lpmsj/work/b/n;)V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    if-ne v0, v1, :cond_4

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->M()Z

    move-result v1

    if-nez v1, :cond_0

    :cond_4
    const/4 v1, 0x3

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    const/4 v2, 0x4

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    invoke-virtual {v0, v1, v2, v6}, Lpmsj/work/b/v;->b(IIZ)I

    goto :goto_0
.end method

.method private static aj(Lpmsj/work/main/w;)V
    .locals 9

    const/16 v8, 0x131

    const/4 v1, 0x3

    const/4 v7, 0x0

    const/4 v4, 0x1

    const/4 v2, 0x2

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    sub-int/2addr v0, v2

    new-array v1, v0, [La/c/i;

    move v2, v7

    :goto_1
    if-ge v2, v0, :cond_1

    add-int/lit8 v3, v2, 0x2

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    aput-object v3, v1, v2

    add-int/lit8 v2, v2, 0x1

    goto :goto_1

    :cond_1
    sget-object v0, Lpmsj/work/b/aa;->a:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x5c

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    aget-object v0, v1, v4

    invoke-virtual {v0}, La/c/i;->b()I

    move-result v0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/b/m;->o(I)Lpmsj/work/b/v;

    move-result-object v1

    if-eqz v1, :cond_2

    iget-object v1, v1, Lpmsj/work/b/v;->E:Lpmsj/work/b/u;

    if-eqz v1, :cond_2

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/m;->w()V

    :cond_2
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/ab;->Z()Z

    move-result v1

    if-eqz v1, :cond_0

    invoke-static {v0}, Lpmsj/work/b/aa;->g(I)Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x51

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    goto :goto_0

    :pswitch_2
    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    if-eqz v0, :cond_0

    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    sub-int/2addr v1, v2

    div-int/2addr v1, v0

    move v2, v7

    :goto_2
    if-ge v2, v0, :cond_4

    new-array v3, v1, [La/c/i;

    mul-int v4, v2, v1

    add-int/lit8 v4, v4, 0x2

    move v5, v7

    :goto_3
    if-ge v5, v1, :cond_3

    add-int v6, v4, v5

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v6

    aput-object v6, v3, v5

    add-int/lit8 v5, v5, 0x1

    goto :goto_3

    :cond_3
    sget-object v4, Lpmsj/work/b/aa;->a:Ljava/util/Vector;

    invoke-virtual {v4, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_2

    :cond_4
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v8}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/b/ab;->E:Lpmsj/work/b/u;

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/m;->w()V

    goto/16 :goto_0

    :pswitch_3
    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    sub-int/2addr v0, v2

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-static {v1}, Lpmsj/work/b/aa;->b(I)[La/c/i;

    move-result-object v1

    if-eqz v1, :cond_0

    move v2, v7

    :goto_4
    if-ge v2, v0, :cond_5

    add-int/lit8 v3, v2, 0x2

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    aput-object v3, v1, v2

    add-int/lit8 v2, v2, 0x1

    goto :goto_4

    :cond_5
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v8}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :pswitch_4
    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/aa;->b(I)[La/c/i;

    move-result-object v0

    if-eqz v0, :cond_0

    aget-object v0, v0, v1

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {v0, v1}, La/c/i;->a(I)V

    goto/16 :goto_0

    :pswitch_5
    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/aa;->b(I)[La/c/i;

    move-result-object v0

    if-eqz v0, :cond_0

    const/4 v1, 0x6

    aget-object v0, v0, v1

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {v0, v1}, La/c/i;->a(I)V

    goto/16 :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_0
        :pswitch_2
        :pswitch_0
        :pswitch_3
        :pswitch_4
        :pswitch_5
    .end packed-switch
.end method

.method private static ak(Lpmsj/work/main/w;)V
    .locals 6

    const/4 v3, 0x0

    const-string v4, " *0"

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    sparse-switch v0, :sswitch_data_0

    :cond_0
    :goto_0
    return-void

    :sswitch_0
    invoke-static {v3, v3}, Lpmsj/work/main/t;->a(ZZ)V

    const/4 v0, 0x3

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuffer;

    invoke-direct {v1}, Ljava/lang/StringBuffer;-><init>()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    invoke-virtual {v2}, Lpmsj/work/b/ab;->q()Z

    move-result v2

    if-eqz v2, :cond_1

    const-string v2, "_*3"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, " *0"

    invoke-virtual {v1, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "\u5411\u60a8\u6c42\u5a5a!"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :goto_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    const/16 v2, 0x2b

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v3

    const-string v4, "\u6211\u613f\u610f"

    const-string v5, "\u4e0d\u613f\u610f"

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/d/n;->b(Ljava/lang/String;ILpmsj/work/d/c;Ljava/lang/String;Ljava/lang/String;)Lpmsj/work/e/aa;

    move-result-object v0

    new-instance v1, Lpmsj/work/a/i;

    const v2, 0x5aa320

    invoke-direct {v1, v2}, Lpmsj/work/a/i;-><init>(I)V

    invoke-virtual {v0, v1}, Lpmsj/work/e/aa;->a(Lpmsj/work/a/i;)V

    invoke-virtual {v0}, Lpmsj/work/e/aa;->i()V

    goto :goto_0

    :cond_1
    const-string v2, "_"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v2, "\u60a8\u5411"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v2, "*3"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, " *0"

    invoke-virtual {v1, v4}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "\u6c42\u5a5a!"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    goto :goto_1

    :sswitch_1
    move v0, v3

    :goto_2
    const/4 v1, 0x2

    if-ge v0, v1, :cond_0

    add-int/lit8 v1, v0, 0x1

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v2

    invoke-virtual {v2, v1}, Lpmsj/work/b/m;->o(I)Lpmsj/work/b/v;

    move-result-object v1

    if-eqz v1, :cond_2

    const v2, 0x227c20

    invoke-virtual {v1, v2, v3}, Lpmsj/work/b/v;->c(IZ)La/a/d;

    :cond_2
    add-int/lit8 v0, v0, 0x1

    goto :goto_2

    nop

    :sswitch_data_0
    .sparse-switch
        0x2 -> :sswitch_0
        0x6 -> :sswitch_1
    .end sparse-switch
.end method

.method private static al(Lpmsj/work/main/w;)V
    .locals 4

    const/16 v1, 0x49

    const/16 v3, 0x46

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v3, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v3, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_4
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_5
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_6
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x2c

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    :pswitch_7
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v3, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_8
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v3, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_9
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x265

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_0
        :pswitch_9
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_2
        :pswitch_0
        :pswitch_3
        :pswitch_0
        :pswitch_0
        :pswitch_4
        :pswitch_6
        :pswitch_8
        :pswitch_7
        :pswitch_5
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_9
    .end packed-switch
.end method

.method private static am(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x1

    const/4 v0, 0x0

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    const/16 v1, 0x36

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v2

    invoke-virtual {v0, v1, v2}, Lpmsj/work/b/ab;->a(BLjava/lang/Object;)V

    goto :goto_0

    :pswitch_2
    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    const/16 v1, 0xa

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v2

    invoke-virtual {v0, v1, v2}, Lpmsj/work/b/ab;->a(BLjava/lang/Object;)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_0
        :pswitch_2
    .end packed-switch
.end method

.method private static an(Lpmsj/work/main/w;)V
    .locals 11

    const/4 v10, 0x4

    const/4 v4, 0x3

    const/4 v3, 0x2

    const/4 v7, 0x1

    const/4 v9, 0x0

    invoke-static {v9, v9}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    if-lez v0, :cond_0

    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    sub-int/2addr v1, v3

    div-int/2addr v1, v0

    move v2, v9

    :goto_1
    if-ge v2, v0, :cond_1

    mul-int v3, v2, v1

    add-int/lit8 v3, v3, 0x2

    invoke-static {v1, v3, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v3

    new-instance v4, Lpmsj/work/b/w;

    sget-byte v5, Lpmsj/work/b/w;->b:B

    aget-object v5, v3, v5

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v5

    invoke-direct {v4, v5, v3}, Lpmsj/work/b/w;-><init>(I[La/c/i;)V

    sget-object v5, Lpmsj/work/b/f;->m:Lpmsj/work/b/y;

    sget-byte v6, Lpmsj/work/b/w;->b:B

    aget-object v3, v3, v6

    invoke-virtual {v3}, La/c/i;->b()I

    move-result v3

    invoke-virtual {v5, v3, v4}, Lpmsj/work/b/y;->a(ILpmsj/work/b/w;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_1

    :cond_1
    if-ne v0, v7, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0xcb

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0xb3

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x25a

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    goto :goto_0

    :pswitch_2
    sget-object v0, Lpmsj/work/b/f;->m:Lpmsj/work/b/y;

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/b/y;->a(IILjava/lang/String;)Lpmsj/work/b/w;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0x1a

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/l;

    if-eqz p0, :cond_0

    invoke-virtual {p0, v0}, Lpmsj/work/e/l;->a(Lpmsj/work/b/w;)V

    goto :goto_0

    :pswitch_3
    sget-object v0, Lpmsj/work/b/f;->m:Lpmsj/work/b/y;

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/b/y;->b(IILjava/lang/String;)Lpmsj/work/b/w;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0xcb

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/du;

    if-eqz p0, :cond_2

    invoke-virtual {p0, v0}, Lpmsj/work/e/du;->b(Lpmsj/work/b/w;)V

    :cond_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const/16 v2, 0xb3

    invoke-virtual {v1, v2}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/dx;

    if-eqz p0, :cond_3

    invoke-virtual {p0, v0}, Lpmsj/work/e/dx;->a(Lpmsj/work/b/w;)V

    :cond_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x25a

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/dw;

    if-eqz p0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/dw;->i()V

    goto/16 :goto_0

    :pswitch_4
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x25a

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/dw;

    if-eqz p0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/dw;->j()V

    goto/16 :goto_0

    :pswitch_5
    invoke-static {v9, v9}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0xb2

    invoke-virtual {v0, v1, p0, v9}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_0

    :pswitch_6
    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/f;->a(I)Lpmsj/work/b/u;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/u;->a(B)V

    iget-object v1, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    if-nez v1, :cond_4

    new-instance v1, Lpmsj/work/b/y;

    invoke-direct {v1}, Lpmsj/work/b/y;-><init>()V

    iput-object v1, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    :cond_4
    new-instance v1, Lpmsj/work/b/y;

    invoke-direct {v1}, Lpmsj/work/b/y;-><init>()V

    iget-object v2, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v2}, Lpmsj/work/b/y;->a()I

    move-result v2

    if-eqz v2, :cond_6

    move v2, v9

    :goto_2
    iget-object v3, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v3}, Lpmsj/work/b/y;->a()I

    move-result v3

    if-ge v2, v3, :cond_5

    iget-object v3, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v3, v2}, Lpmsj/work/b/y;->a(I)Lpmsj/work/b/w;

    move-result-object v3

    invoke-virtual {v1, v3}, Lpmsj/work/b/y;->a(Lpmsj/work/b/w;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_2

    :cond_5
    iget-object v2, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v2}, Lpmsj/work/b/y;->b()V

    :cond_6
    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    if-lez v2, :cond_0

    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3}, Ljava/util/Vector;->size()I

    move-result v3

    sub-int/2addr v3, v10

    div-int/2addr v3, v2

    move v4, v9

    :goto_3
    if-ge v4, v2, :cond_7

    mul-int v5, v4, v3

    add-int/lit8 v5, v5, 0x4

    invoke-static {v3, v5, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v5

    new-instance v6, Lpmsj/work/b/w;

    sget-byte v7, Lpmsj/work/b/w;->b:B

    aget-object v7, v5, v7

    invoke-virtual {v7}, La/c/i;->b()I

    move-result v7

    invoke-direct {v6, v7, v5}, Lpmsj/work/b/w;-><init>(I[La/c/i;)V

    iget-object v7, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    sget-byte v8, Lpmsj/work/b/w;->b:B

    aget-object v5, v5, v8

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v5

    invoke-virtual {v7, v5, v6}, Lpmsj/work/b/y;->a(ILpmsj/work/b/w;)V

    add-int/lit8 v4, v4, 0x1

    goto :goto_3

    :cond_7
    move v2, v9

    :goto_4
    iget-object v3, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v3}, Lpmsj/work/b/y;->a()I

    move-result v3

    if-ge v2, v3, :cond_a

    iget-object v3, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v3, v2}, Lpmsj/work/b/y;->a(I)Lpmsj/work/b/w;

    move-result-object v3

    sget-byte v4, Lpmsj/work/b/w;->l:B

    invoke-virtual {v3, v4}, Lpmsj/work/b/w;->b(I)I

    move-result v4

    if-eq v4, v10, :cond_8

    sget-byte v4, Lpmsj/work/b/w;->l:B

    invoke-virtual {v3, v4}, Lpmsj/work/b/w;->b(I)I

    move-result v3

    const/16 v4, 0x8

    if-ne v3, v4, :cond_9

    :cond_8
    invoke-virtual {v1}, Lpmsj/work/b/y;->a()I

    move-result v2

    if-eqz v2, :cond_a

    move v2, v9

    :goto_5
    invoke-virtual {v1}, Lpmsj/work/b/y;->a()I

    move-result v3

    if-ge v2, v3, :cond_a

    iget-object v3, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v1, v2}, Lpmsj/work/b/y;->a(I)Lpmsj/work/b/w;

    move-result-object v4

    invoke-virtual {v3, v4}, Lpmsj/work/b/y;->a(Lpmsj/work/b/w;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_5

    :cond_9
    add-int/lit8 v2, v2, 0x1

    goto :goto_4

    :cond_a
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x20

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x203

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :pswitch_7
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x20

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ei;

    if-eqz v0, :cond_0

    invoke-virtual {v0}, Lpmsj/work/e/ei;->i()Lpmsj/work/b/u;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/u;->u()I

    move-result v1

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    if-ne v1, v2, :cond_0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/u;->a(B)V

    iget-object v1, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    if-nez v1, :cond_b

    new-instance v1, Lpmsj/work/b/y;

    invoke-direct {v1}, Lpmsj/work/b/y;-><init>()V

    iput-object v1, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    :cond_b
    new-instance v1, Lpmsj/work/b/y;

    invoke-direct {v1}, Lpmsj/work/b/y;-><init>()V

    iget-object v2, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v2}, Lpmsj/work/b/y;->a()I

    move-result v2

    if-eqz v2, :cond_d

    move v2, v9

    :goto_6
    iget-object v3, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v3}, Lpmsj/work/b/y;->a()I

    move-result v3

    if-ge v2, v3, :cond_c

    iget-object v3, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v3, v2}, Lpmsj/work/b/y;->a(I)Lpmsj/work/b/w;

    move-result-object v3

    invoke-virtual {v1, v3}, Lpmsj/work/b/y;->a(Lpmsj/work/b/w;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_6

    :cond_c
    iget-object v2, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v2}, Lpmsj/work/b/y;->b()V

    :cond_d
    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    if-lez v2, :cond_0

    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3}, Ljava/util/Vector;->size()I

    move-result v3

    sub-int/2addr v3, v10

    div-int/2addr v3, v2

    move v4, v9

    :goto_7
    if-ge v4, v2, :cond_e

    mul-int v5, v4, v3

    add-int/lit8 v5, v5, 0x4

    invoke-static {v3, v5, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v5

    new-instance v6, Lpmsj/work/b/w;

    sget-byte v7, Lpmsj/work/b/w;->b:B

    aget-object v7, v5, v7

    invoke-virtual {v7}, La/c/i;->b()I

    move-result v7

    invoke-direct {v6, v7, v5}, Lpmsj/work/b/w;-><init>(I[La/c/i;)V

    iget-object v7, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    sget-byte v8, Lpmsj/work/b/w;->b:B

    aget-object v5, v5, v8

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v5

    invoke-virtual {v7, v5, v6}, Lpmsj/work/b/y;->a(ILpmsj/work/b/w;)V

    add-int/lit8 v4, v4, 0x1

    goto :goto_7

    :cond_e
    move v2, v9

    :goto_8
    iget-object v3, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v3}, Lpmsj/work/b/y;->a()I

    move-result v3

    if-ge v2, v3, :cond_11

    iget-object v3, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v3, v2}, Lpmsj/work/b/y;->a(I)Lpmsj/work/b/w;

    move-result-object v3

    sget-byte v4, Lpmsj/work/b/w;->l:B

    invoke-virtual {v3, v4}, Lpmsj/work/b/w;->b(I)I

    move-result v4

    if-eq v4, v10, :cond_f

    sget-byte v4, Lpmsj/work/b/w;->l:B

    invoke-virtual {v3, v4}, Lpmsj/work/b/w;->b(I)I

    move-result v3

    const/16 v4, 0x8

    if-ne v3, v4, :cond_10

    :cond_f
    invoke-virtual {v1}, Lpmsj/work/b/y;->a()I

    move-result v2

    if-eqz v2, :cond_11

    move v2, v9

    :goto_9
    invoke-virtual {v1}, Lpmsj/work/b/y;->a()I

    move-result v3

    if-ge v2, v3, :cond_11

    iget-object v3, v0, Lpmsj/work/b/u;->h:Lpmsj/work/b/y;

    invoke-virtual {v1, v2}, Lpmsj/work/b/y;->a(I)Lpmsj/work/b/w;

    move-result-object v4

    invoke-virtual {v3, v4}, Lpmsj/work/b/y;->a(Lpmsj/work/b/w;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_9

    :cond_10
    add-int/lit8 v2, v2, 0x1

    goto :goto_8

    :cond_11
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0x20

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :pswitch_8
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x20

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ei;

    invoke-virtual {v0}, Lpmsj/work/e/ei;->i()Lpmsj/work/b/u;

    move-result-object v1

    if-eqz v1, :cond_0

    iget-object v2, v1, Lpmsj/work/b/u;->i:Lpmsj/work/b/y;

    if-nez v2, :cond_12

    new-instance v2, Lpmsj/work/b/y;

    invoke-direct {v2}, Lpmsj/work/b/y;-><init>()V

    iput-object v2, v1, Lpmsj/work/b/u;->i:Lpmsj/work/b/y;

    :cond_12
    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    if-lez v2, :cond_13

    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3}, Ljava/util/Vector;->size()I

    move-result v3

    sub-int/2addr v3, v10

    div-int/2addr v3, v2

    move v4, v9

    :goto_a
    if-ge v4, v2, :cond_13

    mul-int v5, v4, v3

    add-int/lit8 v5, v5, 0x4

    invoke-static {v3, v5, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v5

    new-instance v6, Lpmsj/work/b/w;

    sget-byte v7, Lpmsj/work/b/w;->b:B

    aget-object v7, v5, v7

    invoke-virtual {v7}, La/c/i;->b()I

    move-result v7

    invoke-direct {v6, v7, v5}, Lpmsj/work/b/w;-><init>(I[La/c/i;)V

    iget-object v7, v1, Lpmsj/work/b/u;->i:Lpmsj/work/b/y;

    sget-byte v8, Lpmsj/work/b/w;->b:B

    aget-object v5, v5, v8

    invoke-virtual {v5}, La/c/i;->b()I

    move-result v5

    invoke-virtual {v7, v5, v6}, Lpmsj/work/b/y;->a(ILpmsj/work/b/w;)V

    add-int/lit8 v4, v4, 0x1

    goto :goto_a

    :cond_13
    invoke-virtual {v0}, Lpmsj/work/e/ei;->o()V

    goto/16 :goto_0

    :pswitch_9
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x172

    invoke-virtual {v0, v1, p0, v9}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto/16 :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_2
        :pswitch_5
        :pswitch_0
        :pswitch_3
        :pswitch_4
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_6
        :pswitch_7
        :pswitch_9
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_8
    .end packed-switch
.end method

.method private static ao(Lpmsj/work/main/w;)V
    .locals 8

    const/4 v7, 0x2

    const/4 v6, 0x1

    const/4 v5, 0x0

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->b(I)S

    move-result v2

    const/4 v3, 0x3

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->b(I)S

    move-result v3

    const/4 v4, 0x4

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->f(I)[B

    move-result-object v4

    if-ne v0, v7, :cond_1

    sget-object v0, Lpmsj/work/main/e;->b:[B

    if-eqz v0, :cond_0

    sget-object v0, Lpmsj/work/main/e;->b:[B

    sget-short v2, Lpmsj/work/main/e;->c:S

    invoke-static {v4, v5, v0, v2, v3}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    sget-short v0, Lpmsj/work/main/e;->c:S

    add-int/2addr v0, v3

    int-to-short v0, v0

    sput-short v0, Lpmsj/work/main/e;->c:S

    new-instance v0, La/a/a;

    sget-object v2, Lpmsj/work/main/e;->b:[B

    const v3, 0x927c0

    invoke-direct {v0, v1, v2, v6, v3}, La/a/a;-><init>(I[BZI)V

    sget-object v2, La/a/a;->a:Lpmsj/work/a/l;

    invoke-virtual {v2, v1, v0}, Lpmsj/work/a/l;->a(ILjava/lang/Object;)Ljava/lang/Object;

    const/4 v0, 0x0

    sput-object v0, Lpmsj/work/main/e;->b:[B

    sget-object v0, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "\u83b7\u53d6\u5230dat\u6587\u4ef6"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    :cond_0
    :goto_0
    return-void

    :cond_1
    if-nez v0, :cond_2

    new-array v0, v2, [B

    sput-object v0, Lpmsj/work/main/e;->b:[B

    sput-short v5, Lpmsj/work/main/e;->c:S

    sget-object v0, Lpmsj/work/main/e;->b:[B

    sget-short v1, Lpmsj/work/main/e;->c:S

    invoke-static {v4, v5, v0, v1, v3}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    sget-short v0, Lpmsj/work/main/e;->c:S

    add-int/2addr v0, v3

    int-to-short v0, v0

    sput-short v0, Lpmsj/work/main/e;->c:S

    goto :goto_0

    :cond_2
    sget-object v0, Lpmsj/work/main/e;->b:[B

    if-eqz v0, :cond_0

    sget-object v0, Lpmsj/work/main/e;->b:[B

    sget-short v1, Lpmsj/work/main/e;->c:S

    invoke-static {v4, v5, v0, v1, v3}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    sget-short v0, Lpmsj/work/main/e;->c:S

    add-int/2addr v0, v3

    int-to-short v0, v0

    sput-short v0, Lpmsj/work/main/e;->c:S

    goto :goto_0
.end method

.method private static ap(Lpmsj/work/main/w;)V
    .locals 15

    const/4 v0, 0x0

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    move-result v11

    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    move-result v4

    const/4 v0, 0x2

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B

    const/4 v0, 0x3

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B

    move-result v10

    const/4 v0, 0x4

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    move-result v12

    const/4 v0, 0x5

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    const/4 v1, 0x6

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->b(I)S

    move-result v1

    const/4 v2, 0x7

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    const/16 v3, 0x8

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v3

    const/16 v5, 0x9

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->b(I)S

    move-result v5

    const/16 v6, 0xa

    invoke-virtual {p0, v6}, Lpmsj/work/main/w;->b(I)S

    move-result v6

    const/16 v7, 0xb

    invoke-virtual {p0, v7}, Lpmsj/work/main/w;->c(I)I

    move-result v7

    const/16 v8, 0xc

    invoke-virtual {p0, v8}, Lpmsj/work/main/w;->c(I)I

    move-result v8

    const/16 v9, 0xd

    invoke-virtual {p0, v9}, Lpmsj/work/main/w;->c(I)I

    move-result v9

    const/16 v13, 0xe

    invoke-virtual {p0, v13}, Lpmsj/work/main/w;->b(I)S

    move-result v13

    const/16 v14, 0xf

    invoke-virtual {p0, v14}, Lpmsj/work/main/w;->f(I)[B

    move-result-object p0

    const/4 v14, 0x2

    if-ne v10, v14, :cond_1

    sget-object v4, Lpmsj/work/main/e;->b:[B

    if-eqz v4, :cond_0

    const/4 v4, 0x0

    sget-object v10, Lpmsj/work/main/e;->b:[B

    sget-short v14, Lpmsj/work/main/e;->c:S

    invoke-static {p0, v4, v10, v14, v13}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    invoke-static {v5, v3, v6}, La/a/f;->a(III)I

    move-result p0

    sget-short v4, Lpmsj/work/main/e;->c:S

    add-int/2addr v4, v13

    int-to-short v4, v4

    sput-short v4, Lpmsj/work/main/e;->c:S

    new-array v10, p0, [B

    sget-object v4, Lpmsj/work/main/e;->b:[B

    invoke-static/range {v0 .. v10}, La/a/f;->a(IIII[BIIIII[B)V

    sget-object p0, Ljava/lang/System;->out:Ljava/io/PrintStream;

    new-instance v0, Ljava/lang/StringBuilder;

    invoke-direct {v0}, Ljava/lang/StringBuilder;-><init>()V

    const-string v1, "\u4e0b\u8f7d\u56fe\u7247\u8d44\u6e90\u6210\u529fid="

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0, v12}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "\u5927\u5c0f\uff1a"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    array-length v1, v10

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p0, v0}, Ljava/io/PrintStream;->println(Ljava/lang/String;)V

    packed-switch v11, :pswitch_data_0

    sget-object p0, La/a/f;->h:La/a/c;

    invoke-virtual {p0, v12, v10}, La/a/c;->a(I[B)V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object p0

    invoke-virtual {p0}, Lpmsj/work/b/m;->a()V

    :goto_0
    const/4 p0, 0x0

    sput-object p0, Lpmsj/work/main/e;->b:[B

    :cond_0
    :goto_1
    return-void

    :pswitch_0
    sget-object p0, La/a/f;->i:La/a/c;

    invoke-virtual {p0, v12, v10}, La/a/c;->a(I[B)V

    goto :goto_0

    :cond_1
    if-nez v10, :cond_2

    new-array v0, v4, [B

    sput-object v0, Lpmsj/work/main/e;->b:[B

    const/4 v0, 0x0

    sput-short v0, Lpmsj/work/main/e;->c:S

    const/4 v0, 0x0

    sget-object v1, Lpmsj/work/main/e;->b:[B

    sget-short v2, Lpmsj/work/main/e;->c:S

    invoke-static {p0, v0, v1, v2, v13}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    sget-short p0, Lpmsj/work/main/e;->c:S

    add-int/2addr p0, v13

    int-to-short p0, p0

    sput-short p0, Lpmsj/work/main/e;->c:S

    goto :goto_1

    :cond_2
    sget-object v0, Lpmsj/work/main/e;->b:[B

    if-eqz v0, :cond_0

    const/4 v0, 0x0

    sget-object v1, Lpmsj/work/main/e;->b:[B

    sget-short v2, Lpmsj/work/main/e;->c:S

    invoke-static {p0, v0, v1, v2, v13}, Ljava/lang/System;->arraycopy(Ljava/lang/Object;ILjava/lang/Object;II)V

    sget-short p0, Lpmsj/work/main/e;->c:S

    add-int/2addr p0, v13

    int-to-short p0, p0

    sput-short p0, Lpmsj/work/main/e;->c:S

    goto :goto_1

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_0
    .end packed-switch
.end method

.method private static aq(Lpmsj/work/main/w;)V
    .locals 5

    const/16 v4, 0x136

    const/4 v3, 0x1

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/main/i;->a()Lpmsj/work/main/i;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/main/i;->e:La/c/t;

    invoke-virtual {v0}, La/c/t;->a()V

    invoke-static {}, Lpmsj/work/main/i;->a()Lpmsj/work/main/i;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/main/i;->e:La/c/t;

    invoke-virtual {v0}, La/c/t;->b()V

    sget-object v0, Lpmsj/work/main/MyMidlet;->a:Lpmsj/work/main/MyMidlet;

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v1

    iput-object v1, v0, Lpmsj/work/main/MyMidlet;->b:Ljava/lang/String;

    sget-object v0, Lpmsj/work/main/MyMidlet;->a:Lpmsj/work/main/MyMidlet;

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v1

    if-eqz v1, :cond_0

    move v1, v3

    :goto_0
    iput-boolean v1, v0, Lpmsj/work/main/MyMidlet;->c:Z

    sget-object v0, Lpmsj/work/main/MyMidlet;->a:Lpmsj/work/main/MyMidlet;

    iget-boolean v0, v0, Lpmsj/work/main/MyMidlet;->c:Z

    if-eqz v0, :cond_1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v4}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const-string v2, "\u5ba2\u6237\u7aef\u5df2\u5347\u7ea7\uff0c\u662f\u5426\u4e0b\u8f7d\u6700\u65b0\u5ba2\u6237\u7aef\uff1f"

    invoke-virtual {v1, v2, v3, v0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    :goto_1
    return-void

    :cond_0
    move v1, v2

    goto :goto_0

    :cond_1
    const-string v0, ""

    invoke-static {v0}, Lpmsj/work/main/i;->b(Ljava/lang/String;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v4}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const-string v2, "\u5ba2\u6237\u7aef\u5df2\u5347\u7ea7\uff0c\u8bf7\u4e0b\u8f7d\u6700\u65b0\u5ba2\u6237\u7aef\uff01"

    invoke-virtual {v1, v2, v3, v0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    goto :goto_1
.end method

.method private static ar(Lpmsj/work/main/w;)V
    .locals 4

    const v3, 0x21dfe0

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->c(I)I

    move-result v0

    sget-object v1, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v1}, Lpmsj/work/b/ab;->u()I

    move-result v1

    if-ne v1, v0, :cond_1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x1f

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    sget-object v0, Lpmsj/work/b/f;->a:Lpmsj/work/b/ab;

    invoke-virtual {v0, v3, v2}, Lpmsj/work/b/ab;->c(IZ)La/a/d;

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v0

    const/16 v1, 0xc

    invoke-static {v1, v2, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v1

    const/4 v2, 0x1

    invoke-virtual {v0, v1, v2}, Lpmsj/work/main/k;->a([La/c/i;B)V

    :cond_0
    :goto_0
    return-void

    :cond_1
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/b/m;->n(I)Lpmsj/work/b/v;

    move-result-object v0

    if-eqz v0, :cond_0

    invoke-virtual {v0, v3, v2}, Lpmsj/work/b/v;->c(IZ)La/a/d;

    goto :goto_0
.end method

.method private static as(Lpmsj/work/main/w;)V
    .locals 4

    const/4 v3, 0x0

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    long-to-int v0, v0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    xor-int/2addr v0, v1

    new-instance v1, La/c/r;

    invoke-direct {v1}, La/c/r;-><init>()V

    const/16 v2, 0x3f4

    invoke-virtual {v1, v2}, La/c/r;->a(I)V

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->c(I)I

    move-result v2

    invoke-virtual {v1, v2}, La/c/r;->d(I)V

    invoke-virtual {v1, v0}, La/c/r;->d(I)V

    invoke-virtual {v1, v3}, La/c/r;->d(I)V

    sget-object v0, Lpmsj/work/main/e;->a:Lpmsj/work/main/i;

    invoke-virtual {v1}, La/c/r;->a()[B

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/main/i;->b([B)V

    return-void
.end method

.method private static at(Lpmsj/work/main/w;)V
    .locals 4

    const/4 v0, 0x0

    sput-object v0, Lpmsj/work/b/f;->j:Ljava/util/Vector;

    new-instance v0, Ljava/util/Vector;

    const/4 v1, 0x5

    invoke-direct {v0, v1}, Ljava/util/Vector;-><init>(I)V

    sput-object v0, Lpmsj/work/b/f;->j:Ljava/util/Vector;

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-lez v0, :cond_0

    const/4 v1, 0x0

    :goto_0
    if-ge v1, v0, :cond_0

    sget-object v2, Lpmsj/work/b/f;->j:Ljava/util/Vector;

    iget-object v3, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v3, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    :cond_0
    return-void
.end method

.method private static au(Lpmsj/work/main/w;)V
    .locals 5

    const/16 v4, 0x25d

    const/16 v3, 0x197

    const/16 v2, 0x68

    const/4 v1, 0x0

    invoke-static {v1, v1}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v2, p0, v1}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v2, p0, v1}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v2, p0, v1}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_4
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v4, p0, v1}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_5
    invoke-static {v1, v1}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v1, 0x1

    invoke-virtual {v0, v3, p0, v1}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_6
    invoke-static {v1, v1}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v4, p0, v1}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v3, p0, v1}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_2
        :pswitch_2
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_3
        :pswitch_3
        :pswitch_0
        :pswitch_0
        :pswitch_4
        :pswitch_0
        :pswitch_0
        :pswitch_5
        :pswitch_6
        :pswitch_4
    .end packed-switch
.end method

.method private static av(Lpmsj/work/main/w;)V
    .locals 7

    const/4 v6, 0x0

    const/4 v5, 0x0

    invoke-virtual {p0, v5}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    return-void

    :pswitch_0
    invoke-static {v5, v5}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    new-instance v1, Ljava/util/Vector;

    const/4 v2, 0x5

    invoke-direct {v1, v2}, Ljava/util/Vector;-><init>(I)V

    iput-object v1, v0, Lpmsj/work/b/ab;->i:Ljava/util/Vector;

    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    if-lez v0, :cond_0

    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    const/4 v2, 0x3

    sub-int/2addr v1, v2

    div-int/2addr v1, v0

    move v2, v5

    :goto_1
    if-ge v2, v0, :cond_1

    mul-int v3, v2, v1

    add-int/lit8 v3, v3, 0x2

    invoke-static {v1, v3, p0}, La/c/x;->a(IILpmsj/work/main/w;)[La/c/i;

    move-result-object v3

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v4

    iget-object v4, v4, Lpmsj/work/b/ab;->i:Ljava/util/Vector;

    invoke-virtual {v4, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    goto :goto_1

    :cond_1
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    iput-object v6, v2, Lpmsj/work/b/ab;->L:La/b/c;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v2

    mul-int/2addr v0, v1

    add-int/lit8 v0, v0, 0x2

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    iput v0, v2, Lpmsj/work/b/ab;->T:I

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->s()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iget-object v0, v0, Lpmsj/work/b/ab;->L:La/b/c;

    if-eqz v0, :cond_0

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iput-object v6, v0, Lpmsj/work/b/ab;->L:La/b/c;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->ag()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iput v5, v0, Lpmsj/work/b/ab;->T:I

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
    .end packed-switch
.end method

.method private static aw(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x1a4

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x190

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x11b
        :pswitch_0
        :pswitch_1
    .end packed-switch
.end method

.method private static ax(Lpmsj/work/main/w;)V
    .locals 2

    const/4 v0, 0x0

    invoke-static {v0, v0}, Lpmsj/work/main/t;->a(ZZ)V

    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    return-void
.end method

.method private static ay(Lpmsj/work/main/w;)V
    .locals 7

    const/16 v4, 0xd2

    const/4 v3, 0x2

    const/16 v6, 0xcd

    const/4 v2, 0x1

    const/4 v1, 0x0

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    int-to-byte v0, v0

    sput-byte v0, Lpmsj/work/b/a;->d:B

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v1, 0x5

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v6}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v4, p0, v1}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v4, p0, v1}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_4
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    const/4 v1, 0x3

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v2

    packed-switch v2, :pswitch_data_1

    :goto_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    invoke-static {v6, v0}, Lpmsj/work/d/n;->c(II)V

    goto :goto_0

    :pswitch_5
    invoke-static {v0, v1}, Lpmsj/work/b/a;->b(II)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    const/16 v0, 0xb

    invoke-static {v0}, Lpmsj/work/d/n;->h(I)V

    goto :goto_1

    :pswitch_6
    invoke-static {v0, v1}, Lpmsj/work/b/f;->a(II)V

    goto :goto_1

    :pswitch_7
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    move v2, v3

    :goto_2
    if-ge v1, v0, :cond_0

    add-int/lit8 v3, v2, 0x1

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    add-int/lit8 v4, v3, 0x1

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v3

    add-int/lit8 v5, v4, 0x1

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->d(I)I

    move-result v4

    packed-switch v3, :pswitch_data_2

    :goto_3
    add-int/lit8 v1, v1, 0x1

    move v2, v5

    goto :goto_2

    :pswitch_8
    invoke-static {v2, v4}, Lpmsj/work/b/a;->b(II)V

    goto :goto_3

    :pswitch_9
    invoke-static {v2, v4}, Lpmsj/work/b/f;->a(II)V

    goto :goto_3

    :cond_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v6}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :pswitch_a
    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_3

    :cond_1
    :goto_4
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    invoke-static {v6}, Lpmsj/work/d/n;->h(I)V

    goto/16 :goto_0

    :pswitch_b
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    invoke-static {v0}, Lpmsj/work/b/a;->a(I)V

    goto :goto_4

    :pswitch_c
    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v0

    sget-object v1, Lpmsj/work/b/f;->l:Ljava/util/Vector;

    invoke-static {v0, v1}, Lpmsj/work/b/f;->a(ILjava/util/Vector;)Lpmsj/work/b/u;

    move-result-object v0

    if-eqz v0, :cond_1

    sget-object v1, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    invoke-virtual {v1, v0}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    goto :goto_4

    :pswitch_d
    invoke-static {}, Lpmsj/work/b/a;->d()V

    sget-object v0, Lpmsj/work/b/f;->l:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    :goto_5
    if-ge v1, v0, :cond_2

    sget-object v2, Lpmsj/work/b/f;->k:Ljava/util/Vector;

    sget-object v3, Lpmsj/work/b/f;->l:Ljava/util/Vector;

    invoke-virtual {v3, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v3

    invoke-virtual {v2, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_5

    :cond_2
    sget-object v0, Lpmsj/work/b/f;->l:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->removeAllElements()V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v6}, Lpmsj/work/d/n;->a(I)Z

    goto/16 :goto_0

    :pswitch_e
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v4}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u4fe1\u606f\u5df2\u8fc7\u671f\uff0c\u644a\u4e3b\u5df2\u6536\u644a"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto/16 :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_2
        :pswitch_0
        :pswitch_0
        :pswitch_3
        :pswitch_4
        :pswitch_a
        :pswitch_d
        :pswitch_7
        :pswitch_a
        :pswitch_3
        :pswitch_e
    .end packed-switch

    :pswitch_data_1
    .packed-switch 0x0
        :pswitch_5
        :pswitch_6
    .end packed-switch

    :pswitch_data_2
    .packed-switch 0x0
        :pswitch_8
        :pswitch_9
    .end packed-switch

    :pswitch_data_3
    .packed-switch 0x0
        :pswitch_b
        :pswitch_c
    .end packed-switch
.end method

.method private static az(Lpmsj/work/main/w;)V
    .locals 5

    const/4 v2, 0x0

    const/4 v4, 0x2

    const/4 v3, 0x1

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    return-void

    :pswitch_0
    new-instance v0, Lpmsj/work/b/i;

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    const/4 v2, 0x4

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    invoke-direct {v0, v1, v2}, Lpmsj/work/b/i;-><init>(II)V

    move v1, v3

    :goto_1
    iget-object v2, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    if-ge v1, v2, :cond_1

    int-to-byte v2, v1

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->g(I)La/c/i;

    move-result-object v3

    invoke-virtual {v0, v2, v3}, Lpmsj/work/b/i;->a(BLjava/lang/Object;)V

    add-int/lit8 v1, v1, 0x1

    goto :goto_1

    :cond_1
    invoke-virtual {v0, v4}, Lpmsj/work/b/i;->f(B)I

    move-result v1

    const/4 v2, 0x3

    invoke-virtual {v0, v2}, Lpmsj/work/b/i;->f(B)I

    move-result v2

    invoke-virtual {v0, v1, v2}, Lpmsj/work/b/i;->c(II)V

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/b/m;->a(Lpmsj/work/b/i;)V

    goto :goto_0

    :pswitch_1
    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {p0, v4}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    invoke-virtual {v0, v1, v2}, Lpmsj/work/main/k;->a_(II)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/main/k;->s()V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u91c7\u96c6\u4e2d\u65ad!"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto :goto_0

    :pswitch_3
    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/main/k;->r()I

    move-result v0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    if-ne v0, v1, :cond_2

    invoke-static {}, Lpmsj/work/main/k;->a()Lpmsj/work/main/k;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/main/k;->s()V

    :cond_2
    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->d(I)I

    move-result v1

    invoke-virtual {v0, v1}, Lpmsj/work/b/m;->i(I)V

    goto :goto_0

    :pswitch_4
    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    if-eqz v0, :cond_0

    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v1

    sub-int/2addr v1, v4

    div-int/2addr v1, v0

    :goto_2
    if-ge v2, v0, :cond_0

    mul-int v3, v2, v1

    add-int/lit8 v3, v3, 0x2

    invoke-virtual {p0, v1, v3}, Lpmsj/work/main/w;->a(II)La/c/a;

    move-result-object v3

    sget-object v4, Lpmsj/work/b/p;->b:Ljava/util/Vector;

    invoke-virtual {v4, v3}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    add-int/lit8 v2, v2, 0x1

    int-to-byte v2, v2

    goto :goto_2

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_3
        :pswitch_4
    .end packed-switch
.end method

.method private static b(II)I
    .locals 5

    const/4 v4, 0x0

    sget-object v0, Lpmsj/work/b/f;->v:[Ljava/util/Vector;

    aget-object v1, v0, p1

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v2

    move v3, v4

    :goto_0
    if-ge v3, v2, :cond_1

    invoke-virtual {v1, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-virtual {v0, v4}, La/c/a;->a(I)I

    move-result v0

    if-ne p0, v0, :cond_0

    move v0, v3

    :goto_1
    return v0

    :cond_0
    add-int/lit8 v0, v3, 0x1

    int-to-byte v0, v0

    move v3, v0

    goto :goto_0

    :cond_1
    const/4 v0, -0x1

    goto :goto_1
.end method

.method public static b(I)V
    .locals 2

    const/16 v0, 0x3f1

    const/4 v1, 0x3

    invoke-static {v0, v1, p0}, Lpmsj/work/main/w;->a(ISI)V

    return-void
.end method

.method private static b(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x1

    const/4 v0, 0x0

    invoke-static {v0, v0}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    const/4 v1, 0x2

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v1

    if-nez v0, :cond_1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    :cond_0
    :goto_0
    return-void

    :cond_1
    if-ne v0, v2, :cond_0

    invoke-static {v1}, Lpmsj/work/main/i;->b(Ljava/lang/String;)V

    goto :goto_0
.end method

.method public static c(I)V
    .locals 2

    const/16 v0, 0x408

    const/4 v1, 0x1

    invoke-static {v0, v1, p0}, Lpmsj/work/main/w;->a(IBI)V

    return-void
.end method

.method private static c(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x177

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_1
        :pswitch_0
        :pswitch_1
        :pswitch_1
    .end packed-switch
.end method

.method public static d(I)V
    .locals 3

    const/4 v2, 0x2

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v0

    invoke-virtual {v0, p0}, Lpmsj/work/b/m;->n(I)Lpmsj/work/b/v;

    move-result-object v0

    if-eqz v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    const/16 v1, 0x441

    invoke-static {v1, v2, p0}, Lpmsj/work/main/w;->a(IBI)V

    const/16 v1, 0x517

    invoke-static {v1, v0, p0}, Lpmsj/work/main/w;->a(IBI)V

    return-void

    :cond_0
    move v0, v2

    goto :goto_0
.end method

.method private static d(Lpmsj/work/main/w;)V
    .locals 4

    const/4 v0, 0x0

    invoke-static {v0, v0}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    sget v0, Lpmsj/work/main/i;->q:I

    invoke-static {v0}, Lpmsj/work/main/i;->c(I)V

    const-string v0, "CMNET"

    sget-boolean v1, Lpmsj/work/main/i;->a:Z

    if-nez v1, :cond_0

    const-string v0, "CMWAP"

    :cond_0
    invoke-static {}, Lpmsj/work/main/d;->a()Lpmsj/work/main/d;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/main/d;->c()V

    invoke-static {}, Lpmsj/work/main/d;->a()Lpmsj/work/main/d;

    move-result-object v1

    new-instance v2, Ljava/lang/StringBuilder;

    invoke-direct {v2}, Ljava/lang/StringBuilder;-><init>()V

    const-string v3, "\u8fde\u63a5\u6210\u529f\uff0c\u5f53\u524d\u7f51\u7edc\uff1a"

    invoke-virtual {v2, v3}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v2

    invoke-virtual {v2, v0}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/main/d;->a(Ljava/lang/String;)V

    const/4 v0, 0x1

    sput-boolean v0, Lpmsj/work/main/t;->p:Z

    return-void
.end method

.method private static e(I)I
    .locals 5

    const/4 v4, 0x4

    const/4 v3, 0x3

    const/4 v2, 0x2

    const/4 v1, 0x1

    const/4 v0, -0x1

    if-ne p0, v1, :cond_1

    const/4 v0, 0x0

    :cond_0
    :goto_0
    return v0

    :cond_1
    if-ne p0, v2, :cond_2

    move v0, v1

    goto :goto_0

    :cond_2
    if-ne p0, v3, :cond_3

    move v0, v2

    goto :goto_0

    :cond_3
    if-ne p0, v4, :cond_4

    move v0, v3

    goto :goto_0

    :cond_4
    const/4 v1, 0x6

    if-ne p0, v1, :cond_0

    move v0, v4

    goto :goto_0
.end method

.method private static e(Lpmsj/work/main/w;)V
    .locals 5

    const/16 v4, 0x1f

    const/4 v3, 0x0

    invoke-virtual {p0, v3}, Lpmsj/work/main/w;->b(I)S

    move-result v0

    sparse-switch v0, :sswitch_data_0

    :cond_0
    :goto_0
    invoke-static {v3, v3}, Lpmsj/work/main/t;->a(ZZ)V

    return-void

    :sswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v4}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ei;

    if-eqz p0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/ei;->n()V

    goto :goto_0

    :sswitch_1
    const/4 v0, 0x7

    new-array v0, v0, [I

    move v1, v3

    :goto_1
    array-length v2, v0

    if-ge v1, v2, :cond_1

    add-int/lit8 v2, v1, 0x1

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->d(I)I

    move-result v2

    aput v2, v0, v1

    add-int/lit8 v1, v1, 0x1

    goto :goto_1

    :cond_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v4}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object p0

    check-cast p0, Lpmsj/work/e/ei;

    if-eqz p0, :cond_0

    invoke-virtual {p0, v0}, Lpmsj/work/e/ei;->a([I)V

    goto :goto_0

    :sswitch_data_0
    .sparse-switch
        0x1 -> :sswitch_0
        0x5 -> :sswitch_1
    .end sparse-switch
.end method

.method private static f(I)I
    .locals 4

    const/4 v3, 0x0

    sget-object v0, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v1

    move v2, v3

    :goto_0
    if-ge v2, v1, :cond_1

    sget-object v0, Lpmsj/work/b/f;->w:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, La/c/a;

    invoke-virtual {v0, v3}, La/c/a;->a(I)I

    move-result v0

    if-ne p0, v0, :cond_0

    move v0, v2

    :goto_1
    return v0

    :cond_0
    add-int/lit8 v0, v2, 0x1

    int-to-byte v0, v0

    move v2, v0

    goto :goto_0

    :cond_1
    const/4 v0, -0x1

    goto :goto_1
.end method

.method private static f(Lpmsj/work/main/w;)V
    .locals 2

    const/4 v1, 0x0

    invoke-static {v1, v1}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    sput-byte v1, Lpmsj/work/main/i;->b:B

    const-wide/16 v0, 0x3e8

    :try_start_0
    invoke-static {v0, v1}, Ljava/lang/Thread;->sleep(J)V
    :try_end_0
    .catch Ljava/lang/InterruptedException; {:try_start_0 .. :try_end_0} :catch_0

    :goto_1
    const-string v0, ""

    invoke-static {v0}, Lpmsj/work/main/i;->b(Ljava/lang/String;)V

    goto :goto_0

    :catch_0
    move-exception v0

    goto :goto_1

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
    .end packed-switch
.end method

.method private static g(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v1, 0x7

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x176

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x1
        :pswitch_1
        :pswitch_1
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_1
        :pswitch_2
        :pswitch_2
        :pswitch_2
    .end packed-switch
.end method

.method private static h(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    sparse-switch v0, :sswitch_data_0

    :cond_0
    :goto_0
    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    return-void

    :sswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x21

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ej;

    if-eqz v0, :cond_0

    invoke-virtual {v0, p0}, Lpmsj/work/e/ej;->b(Lpmsj/work/main/w;)V

    goto :goto_0

    :sswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x18d

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :sswitch_data_0
    .sparse-switch
        0x1 -> :sswitch_0
        0x3 -> :sswitch_1
        0x4 -> :sswitch_1
        0x5 -> :sswitch_0
        0xe -> :sswitch_0
        0xf -> :sswitch_0
    .end sparse-switch
.end method

.method private static i(Lpmsj/work/main/w;)V
    .locals 3

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0}, Ljava/lang/StringBuffer;-><init>()V

    const/4 v1, 0x1

    :goto_0
    iget-object v2, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v2}, Ljava/util/Vector;->size()I

    move-result v2

    if-ge v1, v2, :cond_0

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    move-result-object v2

    invoke-virtual {v0, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const/16 v2, 0x5f

    invoke-virtual {v0, v2}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    add-int/lit8 v1, v1, 0x1

    goto :goto_0

    :cond_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    const/16 v2, 0x4e20

    invoke-virtual {v1, v0, v2}, Lpmsj/work/d/n;->a(Ljava/lang/String;I)Lpmsj/work/e/br;

    return-void
.end method

.method private static j(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x184

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_1
        :pswitch_1
        :pswitch_1
    .end packed-switch
.end method

.method private static k(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x183

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
    .end packed-switch
.end method

.method private static l(Lpmsj/work/main/w;)V
    .locals 2

    const/4 v0, 0x0

    invoke-static {v0, v0}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x21

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ej;

    if-eqz v0, :cond_0

    invoke-virtual {v0, p0}, Lpmsj/work/e/ej;->c(Lpmsj/work/main/w;)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_0
        :pswitch_0
    .end packed-switch
.end method

.method private static m(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x5f

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_0
    .end packed-switch
.end method

.method private static n(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v1, 0x1

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x170

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x1e
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_1
    .end packed-switch
.end method

.method private static o(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x164

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x163

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_1
        :pswitch_2
        :pswitch_2
        :pswitch_0
        :pswitch_2
    .end packed-switch
.end method

.method private static p(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x15e

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x15f

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_0
        :pswitch_0
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_2
        :pswitch_2
        :pswitch_2
        :pswitch_2
        :pswitch_2
        :pswitch_2
        :pswitch_2
        :pswitch_2
    .end packed-switch
.end method

.method private static q(Lpmsj/work/main/w;)V
    .locals 1

    const/4 v0, 0x0

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    const/4 v0, 0x1

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    const/4 v0, 0x2

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    const/4 v0, 0x3

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    const/4 v0, 0x4

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    const/4 v0, 0x5

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->c(I)I

    const/4 v0, 0x6

    invoke-virtual {p0, v0}, Lpmsj/work/main/w;->e(I)Ljava/lang/String;

    return-void
.end method

.method private static r(Lpmsj/work/main/w;)V
    .locals 4

    const/16 v1, 0x136

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    sget-object v0, Lpmsj/work/main/MyMidlet;->a:Lpmsj/work/main/MyMidlet;

    iget-boolean v0, v0, Lpmsj/work/main/MyMidlet;->c:Z

    if-nez v0, :cond_0

    const-string v0, ""

    invoke-static {v0}, Lpmsj/work/main/i;->b(Ljava/lang/String;)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    const-string v2, "\u5ba2\u6237\u7aef\u5df2\u5347\u7ea7\uff0c\u8bf7\u4e0b\u8f7d\u6700\u65b0\u5ba2\u6237\u7aef\uff01"

    const/4 v3, 0x1

    invoke-virtual {v1, v2, v3, v0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    :goto_0
    return-void

    :cond_0
    sget v0, Lpmsj/work/main/i;->n:I

    invoke-static {v0}, Lpmsj/work/main/i;->b(I)Z

    move-result v0

    if-eqz v0, :cond_1

    sput-byte v2, Lpmsj/work/main/i;->b:B

    invoke-static {}, Lpmsj/work/main/c;->a()Lpmsj/work/main/c;

    invoke-static {}, Lpmsj/work/main/c;->c()V

    goto :goto_0

    :cond_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(I)Z

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0xa

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0
.end method

.method private static s(Lpmsj/work/main/w;)V
    .locals 4

    const/16 v3, 0xa

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/main/i;->a()Lpmsj/work/main/i;

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    if-nez v0, :cond_0

    iget-object v0, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v0, v2}, Ljava/util/Vector;->removeElementAt(I)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v0, v3}, Lpmsj/work/d/n;->f(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/do;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v3, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    iget-object v1, p0, Lpmsj/work/main/w;->b:Ljava/util/Vector;

    invoke-virtual {v1}, Ljava/util/Vector;->lastElement()Ljava/lang/Object;

    move-result-object p0

    check-cast p0, La/c/p;

    invoke-virtual {p0}, La/c/p;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1, v1, v2, v2}, Lpmsj/work/e/do;->a(Ljava/lang/String;Ljava/lang/String;ZZ)V

    :goto_0
    return-void

    :cond_0
    invoke-static {}, Lpmsj/work/main/i;->a()Lpmsj/work/main/i;

    const-string v0, "\u767b\u5f55\u65f6\u53d1\u751f\u9519\u8bef\uff01"

    invoke-static {v0}, Lpmsj/work/main/i;->b(Ljava/lang/String;)V

    goto :goto_0
.end method

.method private static t(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x167

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_2
    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x169

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x160

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_2
        :pswitch_2
        :pswitch_3
        :pswitch_3
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_3
        :pswitch_2
        :pswitch_2
    .end packed-switch
.end method

.method private static u(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/4 v1, 0x1

    invoke-virtual {p0, v1}, Lpmsj/work/main/w;->c(I)I

    move-result v1

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_0
        :pswitch_1
    .end packed-switch
.end method

.method private static v(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x152

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_1
    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    const/4 v1, 0x0

    iput-object v1, v0, Lpmsj/work/b/ab;->L:La/b/c;

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    invoke-virtual {v0}, Lpmsj/work/b/ab;->ag()V

    invoke-static {}, Lpmsj/work/b/ab;->a()Lpmsj/work/b/ab;

    move-result-object v0

    iput v2, v0, Lpmsj/work/b/ab;->T:I

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x18b

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    invoke-static {v2, v2}, Lpmsj/work/main/t;->a(ZZ)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_1
        :pswitch_2
    .end packed-switch
.end method

.method private static w(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :cond_0
    :goto_0
    :pswitch_0
    return-void

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x25e

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->d(I)Lpmsj/work/d/c;

    move-result-object v0

    check-cast v0, Lpmsj/work/e/ei;

    if-eqz v0, :cond_0

    invoke-virtual {v0, p0}, Lpmsj/work/e/ei;->b(Lpmsj/work/main/w;)V

    goto :goto_0

    :pswitch_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x260

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_1
        :pswitch_1
        :pswitch_1
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_0
        :pswitch_2
        :pswitch_2
        :pswitch_0
        :pswitch_2
    .end packed-switch
.end method

.method private static x(Lpmsj/work/main/w;)V
    .locals 3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x14f

    const/4 v2, 0x0

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    return-void
.end method

.method private static y(Lpmsj/work/main/w;)V
    .locals 3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x14e

    const/4 v2, 0x0

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    return-void
.end method

.method private static z(Lpmsj/work/main/w;)V
    .locals 3

    const/4 v2, 0x0

    invoke-virtual {p0, v2}, Lpmsj/work/main/w;->a(I)B

    move-result v0

    packed-switch v0, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x14c

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    :pswitch_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const/16 v1, 0x14d

    invoke-virtual {v0, v1, p0, v2}, Lpmsj/work/d/n;->a(ILpmsj/work/main/w;Z)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0x0
        :pswitch_0
        :pswitch_1
    .end packed-switch
.end method
