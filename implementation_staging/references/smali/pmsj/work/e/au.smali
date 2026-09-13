.class public final Lpmsj/work/e/au;
.super Lpmsj/work/e/at;


# instance fields
.field private Y:B

.field private Z:[Ljava/lang/String;

.field private aa:Ljava/util/Vector;

.field private ab:I

.field private ac:Lpmsj/work/b/g;

.field private ad:Z

.field private final ae:B

.field private final af:B

.field private final ag:B

.field private final ah:B

.field private final ai:B

.field private aj:Ljava/lang/String;

.field private ak:I

.field private al:B

.field private am:J


# direct methods
.method public constructor <init>()V
    .locals 2

    invoke-direct {p0}, Lpmsj/work/e/at;-><init>()V

    const/16 v0, 0xa

    iput-byte v0, p0, Lpmsj/work/e/au;->ae:B

    const/16 v0, 0xb

    iput-byte v0, p0, Lpmsj/work/e/au;->af:B

    const/16 v0, 0xc

    iput-byte v0, p0, Lpmsj/work/e/au;->ag:B

    const/16 v0, 0xd

    iput-byte v0, p0, Lpmsj/work/e/au;->ah:B

    const/16 v0, 0xe

    iput-byte v0, p0, Lpmsj/work/e/au;->ai:B

    const/4 v0, -0x1

    iput v0, p0, Lpmsj/work/e/au;->ak:I

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    iput-wide v0, p0, Lpmsj/work/e/au;->am:J

    return-void
.end method

.method private au()V
    .locals 3

    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    :goto_0
    iget v1, p0, Lpmsj/work/e/au;->ab:I

    sub-int v0, v1, v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "\u8fd8\u53ef\u9009\u62e9"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, v0}, Ljava/lang/StringBuilder;->append(I)Ljava/lang/StringBuilder;

    move-result-object v0

    const-string v1, "\u4e2a"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v0

    invoke-virtual {v0}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p0, v0}, Lpmsj/work/e/au;->d(Ljava/lang/String;)V

    return-void

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method private b(Ljava/lang/String;I)V
    .locals 2

    new-instance v0, Ljava/lang/StringBuffer;

    invoke-direct {v0, p1}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    const-string v1, "*"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    if-lez p2, :cond_0

    sget-byte v1, Lpmsj/work/a/c;->o:B

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    const-string v1, "+"

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    :goto_0
    invoke-virtual {v0, p2}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    iget-object v1, p0, Lpmsj/work/e/au;->c:Lpmsj/work/d/l;

    invoke-virtual {v0}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->d(Ljava/lang/String;)V

    return-void

    :cond_0
    sget-byte v1, Lpmsj/work/a/c;->n:B

    invoke-virtual {v0, v1}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    goto :goto_0
.end method

.method private static c(Lpmsj/work/b/j;)V
    .locals 4

    const/4 v0, 0x2

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v1

    invoke-virtual {v1}, Lpmsj/work/b/m;->h()I

    move-result v1

    iget v2, p0, Lpmsj/work/b/j;->e:I

    const/4 v3, 0x1

    invoke-static {v0, v1, v2, v3}, Lpmsj/work/main/e;->a(BIIS)V

    return-void
.end method

.method private d(Lpmsj/work/b/j;)Z
    .locals 4

    const/4 v3, 0x0

    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    if-nez v0, :cond_0

    move v0, v3

    :goto_0
    return v0

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    move v1, v3

    :goto_1
    if-ge v1, v0, :cond_2

    iget-object v2, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    invoke-virtual {v2, v1}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v2

    if-ne p1, v2, :cond_1

    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Ljava/util/Vector;->removeElementAt(I)V

    const/4 v0, 0x1

    goto :goto_0

    :cond_1
    add-int/lit8 v1, v1, 0x1

    goto :goto_1

    :cond_2
    move v0, v3

    goto :goto_0
.end method

.method private e(Lpmsj/work/b/j;)V
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    if-eqz v0, :cond_2

    invoke-direct {p0, p1}, Lpmsj/work/e/au;->d(Lpmsj/work/b/j;)Z

    move-result v0

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->Q()V

    invoke-direct {p0}, Lpmsj/work/e/au;->au()V

    :goto_0
    return-void

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    iget v1, p0, Lpmsj/work/e/au;->ab:I

    if-ge v0, v1, :cond_1

    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    invoke-virtual {v0, p1}, Ljava/util/Vector;->addElement(Ljava/lang/Object;)V

    const v0, 0x3ce1f0

    const/4 v1, 0x0

    invoke-static {v0, v1}, Lpmsj/work/a/k;->b(II)Ljava/lang/String;

    move-result-object v0

    iget-object v1, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    invoke-virtual {v1, v0}, Lpmsj/work/d/l;->h(Ljava/lang/String;)V

    invoke-direct {p0}, Lpmsj/work/e/au;->au()V

    goto :goto_0

    :cond_1
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    iget-object v1, p0, Lpmsj/work/e/au;->aj:Ljava/lang/String;

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto :goto_0

    :cond_2
    invoke-direct {p0, p1}, Lpmsj/work/e/au;->f(Lpmsj/work/b/j;)V

    goto :goto_0
.end method

.method private f(Lpmsj/work/b/j;)V
    .locals 4

    iget-object v0, p0, Lpmsj/work/e/au;->r:Lpmsj/work/d/c;

    invoke-virtual {v0, p1}, Lpmsj/work/d/c;->a(Lpmsj/work/b/j;)Z

    move-result v0

    if-eqz v0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/au;->ae()V

    iget-object v0, p0, Lpmsj/work/e/au;->r:Lpmsj/work/d/c;

    instance-of v0, v0, Lpmsj/work/e/w;

    if-eqz v0, :cond_0

    iget-object p0, p0, Lpmsj/work/e/au;->r:Lpmsj/work/d/c;

    check-cast p0, Lpmsj/work/e/w;

    invoke-virtual {p0}, Lpmsj/work/e/w;->i()Ljava/lang/String;

    move-result-object v0

    const-string v1, "\u804a\u5929"

    const/16 v2, 0x50

    const/4 v3, 0x0

    invoke-static {v1, v2, v3, v0, p0}, Lpmsj/work/c/a;->a(Ljava/lang/String;IILjava/lang/String;Lpmsj/work/a/a;)V

    :cond_0
    return-void
.end method


# virtual methods
.method protected final C(I)V
    .locals 5

    const/4 v1, 0x3

    const/4 v4, 0x1

    if-eqz p1, :cond_1

    invoke-virtual {p0, p1}, Lpmsj/work/e/au;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    check-cast v0, Lpmsj/work/d/k;

    iput-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->c()V

    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {v0, v1, v1}, Lpmsj/work/d/k;->a(II)V

    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    sget-object v1, Lpmsj/work/a/c;->an:[Ljava/lang/String;

    invoke-virtual {v0, v1}, Lpmsj/work/d/k;->a([Ljava/lang/String;)V

    iget-object v0, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    iget-object v1, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->a(Lpmsj/work/d/k;)V

    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    const v1, 0x800090

    invoke-virtual {v0, v1}, Lpmsj/work/d/k;->l(I)V

    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    new-instance v1, Lpmsj/work/a/i;

    const v2, 0x10f656

    invoke-direct {v1, v2, v4}, Lpmsj/work/a/i;-><init>(II)V

    new-instance v2, Lpmsj/work/a/i;

    const v3, 0x10f4c6

    invoke-direct {v2, v3, v4}, Lpmsj/work/a/i;-><init>(II)V

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/k;->a(Lpmsj/work/a/i;Lpmsj/work/a/i;)V

    const/4 v0, 0x0

    :goto_0
    iget-object v1, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {v1}, Lpmsj/work/d/k;->h()I

    move-result v1

    if-ge v0, v1, :cond_0

    add-int/lit8 v1, v0, 0xa

    iget-object v2, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {p0, v1, v2}, Lpmsj/work/e/au;->a(ILpmsj/work/d/b;)V

    add-int/lit8 v0, v0, 0x1

    goto :goto_0

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    const/high16 v1, 0x80000

    invoke-virtual {v0, v1}, Lpmsj/work/d/k;->l(I)V

    :cond_1
    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    if-nez v0, :cond_2

    move v0, v4

    :goto_1
    new-array v0, v0, [Ljava/util/Vector;

    iput-object v0, p0, Lpmsj/work/e/au;->e:[Ljava/util/Vector;

    return-void

    :cond_2
    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {v0}, Lpmsj/work/d/k;->h()I

    move-result v0

    add-int/lit8 v0, v0, 0x1

    goto :goto_1
.end method

.method public final E(I)V
    .locals 0

    iput p1, p0, Lpmsj/work/e/au;->ab:I

    invoke-direct {p0}, Lpmsj/work/e/au;->au()V

    return-void
.end method

.method public final a(Ljava/util/Vector;B[Ljava/lang/String;Ljava/util/Vector;ILpmsj/work/b/g;IIZLjava/lang/String;)V
    .locals 5

    const/4 v4, 0x2

    const/4 v3, 0x0

    const/16 v0, 0x10

    invoke-virtual {p0, v0}, Lpmsj/work/e/au;->r(I)V

    invoke-virtual {p0, p10}, Lpmsj/work/e/au;->d(Ljava/lang/String;)V

    iput-object p10, p0, Lpmsj/work/e/au;->aj:Ljava/lang/String;

    iput-byte p2, p0, Lpmsj/work/e/au;->Y:B

    iput-object p3, p0, Lpmsj/work/e/au;->Z:[Ljava/lang/String;

    iput-object p4, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    iput-object p6, p0, Lpmsj/work/e/au;->ac:Lpmsj/work/b/g;

    iput-boolean p9, p0, Lpmsj/work/e/au;->ad:Z

    iget-object v0, p0, Lpmsj/work/e/au;->c:Lpmsj/work/d/l;

    invoke-virtual {v0, p8}, Lpmsj/work/d/l;->c(I)V

    iget-byte v0, p0, Lpmsj/work/e/au;->Y:B

    if-lez v0, :cond_5

    if-lez p5, :cond_3

    invoke-virtual {p0, p5}, Lpmsj/work/e/au;->E(I)V

    :goto_0
    const-string v0, "\u9009\u62e9"

    invoke-virtual {p0, v0}, Lpmsj/work/e/au;->e(Ljava/lang/String;)V

    if-eqz p4, :cond_0

    const-string v0, "\u5b8c\u6210"

    invoke-virtual {p0, v0}, Lpmsj/work/e/au;->f(Ljava/lang/String;)V

    :cond_0
    iput-object p1, p0, Lpmsj/work/e/au;->V:Ljava/util/Vector;

    iget-byte v0, p0, Lpmsj/work/e/au;->Y:B

    if-lez v0, :cond_6

    iget-byte v0, p0, Lpmsj/work/e/au;->Y:B

    iget-object v1, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {v1}, Lpmsj/work/d/k;->h()I

    move-result v1

    if-eq v0, v1, :cond_1

    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    iget-object v1, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    iget v1, v1, Lpmsj/work/d/b;->k:I

    iget-byte v2, p0, Lpmsj/work/e/au;->Y:B

    mul-int/2addr v1, v2

    iget-object v2, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {v2}, Lpmsj/work/d/k;->h()I

    move-result v2

    div-int/2addr v1, v2

    iput v1, v0, Lpmsj/work/d/b;->k:I

    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    iget-byte v1, p0, Lpmsj/work/e/au;->Y:B

    invoke-virtual {v0, v1}, Lpmsj/work/d/k;->a(I)V

    :cond_1
    :goto_1
    invoke-virtual {p0}, Lpmsj/work/e/au;->ag()V

    if-eqz p7, :cond_2

    invoke-virtual {p0}, Lpmsj/work/e/au;->j()Ljava/util/Vector;

    move-result-object v1

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v2

    :goto_2
    if-ge v3, v2, :cond_2

    invoke-virtual {v1, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/j;

    iget v0, v0, Lpmsj/work/b/j;->e:I

    if-ne v0, p7, :cond_8

    iget-object v0, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    invoke-virtual {v0, v3}, Lpmsj/work/d/l;->g(I)V

    :cond_2
    return-void

    :cond_3
    if-eqz p9, :cond_4

    const-string v0, "\u9009\u62e9\u5356\u51fa"

    invoke-virtual {p0, v0}, Lpmsj/work/e/au;->d(Ljava/lang/String;)V

    goto :goto_0

    :cond_4
    const-string v0, "\u9009\u62e9\u7269\u54c1"

    invoke-virtual {p0, v0}, Lpmsj/work/e/au;->d(Ljava/lang/String;)V

    goto :goto_0

    :cond_5
    const-string v0, ""

    invoke-virtual {p0, v0}, Lpmsj/work/e/au;->d(Ljava/lang/String;)V

    goto :goto_0

    :cond_6
    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {v0, v3}, Lpmsj/work/d/k;->a(Z)V

    iget-object v0, p0, Lpmsj/work/e/au;->W:Lpmsj/work/d/g;

    invoke-virtual {v0, v3}, Lpmsj/work/d/g;->a(Z)V

    iget-object v0, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    iget v1, p0, Lpmsj/work/e/au;->k:I

    div-int/lit8 v1, v1, 0x3

    mul-int/lit8 v1, v1, 0x2

    iget-object v2, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    iget v2, v2, Lpmsj/work/d/l;->l:I

    mul-int/lit8 v2, v2, 0x5

    div-int/lit8 v2, v2, 0x6

    invoke-virtual {v0, v1, v2}, Lpmsj/work/d/l;->e(II)V

    iget-object v0, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    sget-short v1, Lpmsj/work/main/t;->c:S

    iget v2, p0, Lpmsj/work/d/b;->k:I

    add-int/2addr v1, v2

    div-int/lit8 v1, v1, 0x2

    iget-object v2, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    iget v2, v2, Lpmsj/work/d/b;->k:I

    sub-int/2addr v1, v2

    const/16 v2, 0xf

    sub-int/2addr v1, v2

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->i:S

    iget-object v0, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    iget-object v1, p0, Lpmsj/work/e/au;->c:Lpmsj/work/d/l;

    iget-short v1, v1, Lpmsj/work/d/l;->j:S

    iget-object v2, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    iget v2, v2, Lpmsj/work/d/l;->l:I

    sub-int/2addr v1, v2

    const/4 v2, 0x3

    sub-int/2addr v1, v2

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->j:S

    iget-object v0, p0, Lpmsj/work/e/au;->b:Lpmsj/work/d/l;

    if-eqz v0, :cond_7

    iget-object v0, p0, Lpmsj/work/e/au;->b:Lpmsj/work/d/l;

    invoke-virtual {v0, v3}, Lpmsj/work/d/l;->a(Z)V

    iget-object v0, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    invoke-virtual {v0, v4}, Lpmsj/work/d/l;->l(I)V

    iget-object v0, p0, Lpmsj/work/e/au;->c:Lpmsj/work/d/l;

    invoke-virtual {v0, v4}, Lpmsj/work/d/l;->l(I)V

    :cond_7
    const/16 v0, 0x8

    invoke-virtual {p0, v0}, Lpmsj/work/e/au;->q(I)V

    goto/16 :goto_1

    :cond_8
    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto/16 :goto_2
.end method

.method public final a(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 6

    const/16 v5, 0x23

    invoke-super {p0, p1, p2, p3}, Lpmsj/work/e/at;->a(Ljavax/microedition/lcdui/Graphics;II)V

    iget v0, p0, Lpmsj/work/e/au;->ak:I

    if-lez v0, :cond_1

    invoke-virtual {p0}, Lpmsj/work/e/au;->at()Z

    move-result v0

    if-nez v0, :cond_1

    sget-short v0, Lpmsj/work/main/t;->d:S

    sub-int/2addr v0, v5

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v1

    iget-wide v3, p0, Lpmsj/work/e/au;->am:J

    sub-long/2addr v1, v3

    const-wide/16 v3, 0x190

    cmp-long v1, v1, v3

    if-lez v1, :cond_0

    const/4 v1, 0x2

    sget-byte v2, Lpmsj/work/e/au;->E:B

    add-int/lit8 v2, v2, 0xa

    const/4 v3, 0x1

    invoke-static {p1, v1, v0, v2, v3}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIB)V

    invoke-virtual {p0}, Lpmsj/work/e/au;->U()Ljava/lang/String;

    move-result-object v1

    const/4 v2, 0x7

    sget v3, Lpmsj/work/a/c;->ac:I

    sub-int v3, v5, v3

    div-int/lit8 v3, v3, 0x2

    add-int/2addr v0, v3

    const v3, 0xf8f8a0

    invoke-static {p1, v1, v2, v0, v3}, La/c/x;->b(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;III)V

    :cond_0
    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    iget-wide v2, p0, Lpmsj/work/e/au;->am:J

    sub-long/2addr v0, v2

    const-wide/16 v2, 0x320

    cmp-long v0, v0, v2

    if-lez v0, :cond_1

    invoke-static {}, Ljava/lang/System;->currentTimeMillis()J

    move-result-wide v0

    iput-wide v0, p0, Lpmsj/work/e/au;->am:J

    :cond_1
    return-void
.end method

.method public final a(ILjava/lang/String;)Z
    .locals 9

    const/16 v2, 0xe

    const/16 v1, 0xd

    const/4 v8, 0x1

    const/4 v4, 0x0

    const/16 v0, 0xa

    if-ne v0, p1, :cond_3

    invoke-static {p2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v0

    invoke-virtual {p0}, Lpmsj/work/e/au;->i()Lpmsj/work/b/j;

    move-result-object v1

    if-nez v1, :cond_0

    move v0, v8

    :goto_0
    return v0

    :cond_0
    if-lez v0, :cond_2

    iget-short v2, v1, Lpmsj/work/b/j;->g:S

    if-gt v0, v2, :cond_2

    invoke-direct {p0, v1}, Lpmsj/work/e/au;->f(Lpmsj/work/b/j;)V

    :cond_1
    :goto_1
    move v0, v8

    goto :goto_0

    :cond_2
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8f93\u5165\u7684\u4e2a\u6570\u5927\u4e8e\u7269\u54c1\u6570\u91cf,\u8bf7\u91cd\u65b0\u8f93\u5165"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v4

    goto :goto_0

    :cond_3
    if-eq v1, p1, :cond_4

    if-ne v2, p1, :cond_1

    :cond_4
    invoke-virtual {p2}, Ljava/lang/String;->length()I

    move-result v0

    if-nez v0, :cond_5

    move v0, v4

    goto :goto_0

    :cond_5
    invoke-static {p2}, Ljava/lang/Integer;->parseInt(Ljava/lang/String;)I

    move-result v7

    if-gtz v7, :cond_6

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8f93\u5165\u7684\u4ef7\u683c\u5fc5\u987b\u5927\u4e8e0"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v4

    goto :goto_0

    :cond_6
    invoke-virtual {p0}, Lpmsj/work/e/au;->i()Lpmsj/work/b/j;

    move-result-object v3

    invoke-virtual {v3}, Lpmsj/work/b/j;->n()Z

    move-result v0

    if-eqz v0, :cond_7

    iget-short v0, v3, Lpmsj/work/b/j;->g:S

    move v6, v0

    :goto_2
    if-ne v1, p1, :cond_8

    const/16 v0, 0x472

    new-instance v1, La/c/h;

    const/16 v2, 0x9

    invoke-direct {v1, v2}, La/c/h;-><init>(B)V

    new-instance v2, La/c/m;

    iget v3, v3, Lpmsj/work/b/j;->e:I

    invoke-direct {v2, v3}, La/c/m;-><init>(I)V

    new-instance v3, La/c/h;

    invoke-direct {v3, v8}, La/c/h;-><init>(B)V

    new-instance v4, La/c/m;

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v5

    invoke-virtual {v5}, Lpmsj/work/b/m;->h()I

    move-result v5

    invoke-direct {v4, v5}, La/c/m;-><init>(I)V

    new-instance v5, La/c/h;

    int-to-byte v6, v6

    invoke-direct {v5, v6}, La/c/h;-><init>(B)V

    new-instance v6, La/c/m;

    invoke-direct {v6, v7}, La/c/m;-><init>(I)V

    invoke-static/range {v0 .. v6}, Lpmsj/work/main/w;->a(ILa/c/i;La/c/i;La/c/i;La/c/i;La/c/i;La/c/i;)V

    goto :goto_1

    :cond_7
    move v6, v8

    goto :goto_2

    :cond_8
    if-ne v2, p1, :cond_1

    const/16 v0, 0x6c3

    const/4 v1, 0x5

    iget v2, v3, Lpmsj/work/b/j;->e:I

    invoke-static {v0, v1, v2, v7, v4}, Lpmsj/work/main/w;->a(IBIIB)V

    goto :goto_1
.end method

.method public final ag()V
    .locals 1

    iget-byte v0, p0, Lpmsj/work/e/au;->Y:B

    if-lez v0, :cond_0

    invoke-super {p0}, Lpmsj/work/e/at;->ag()V

    :goto_0
    return-void

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/au;->V:Ljava/util/Vector;

    invoke-virtual {p0, v0}, Lpmsj/work/e/au;->b(Ljava/util/Vector;)V

    invoke-virtual {p0}, Lpmsj/work/e/au;->k()V

    goto :goto_0
.end method

.method protected final aq()V
    .locals 0

    return-void
.end method

.method public final as()V
    .locals 2

    const/4 v1, 0x0

    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {v0, v1}, Lpmsj/work/d/k;->c(I)V

    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    invoke-virtual {v0, v1}, Lpmsj/work/d/k;->h(I)V

    return-void
.end method

.method public final at()Z
    .locals 1

    iget-object v0, p0, Lpmsj/work/e/au;->V:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-lez v0, :cond_0

    const/4 v0, 0x1

    :goto_0
    return v0

    :cond_0
    const/4 v0, 0x0

    goto :goto_0
.end method

.method protected final b(Lpmsj/work/b/j;)V
    .locals 2

    invoke-direct {p0, p1}, Lpmsj/work/e/au;->d(Lpmsj/work/b/j;)Z

    move-result v0

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/d/l;->Q()V

    invoke-direct {p0}, Lpmsj/work/e/au;->au()V

    :goto_0
    return-void

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/au;->Z:[Ljava/lang/String;

    if-eqz v0, :cond_1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    iget-object v1, p0, Lpmsj/work/e/au;->Z:[Ljava/lang/String;

    invoke-virtual {v0, v1, p0}, Lpmsj/work/d/n;->a([Ljava/lang/String;Lpmsj/work/d/c;)V

    goto :goto_0

    :cond_1
    invoke-direct {p0, p1}, Lpmsj/work/e/au;->e(Lpmsj/work/b/j;)V

    goto :goto_0
.end method

.method public final b(Ljava/lang/String;)Z
    .locals 9

    const/4 v6, 0x2

    const/16 v4, 0x20

    const/4 v8, 0x1

    const-string v5, "\u5356\u51fa"

    const-string v3, "\u5bc4\u552e"

    invoke-super {p0, p1}, Lpmsj/work/e/at;->b(Ljava/lang/String;)Z

    invoke-virtual {p0}, Lpmsj/work/e/au;->i()Lpmsj/work/b/j;

    move-result-object v0

    if-nez v0, :cond_0

    move v0, v8

    :goto_0
    return v0

    :cond_0
    const-string v1, "\u5b58\u653e"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_5

    const/16 v1, 0x33

    iget-byte v2, v0, Lpmsj/work/b/j;->k:B

    if-ne v1, v2, :cond_1

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "\u4efb\u52a1\u7269\u54c1\u4e0d\u5141\u8bb8"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v8

    goto :goto_0

    :cond_1
    invoke-virtual {v0, v6}, Lpmsj/work/b/j;->d(I)Z

    move-result v1

    if-eqz v1, :cond_2

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8be5\u7269\u54c1\u4e0d\u5141\u8bb8\u5b58\u653e\u4ed3\u5e93"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    :goto_1
    move v0, v8

    goto :goto_0

    :cond_2
    iget v1, p0, Lpmsj/work/e/au;->ab:I

    if-nez v1, :cond_3

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u4ed3\u5e93\u5df2\u6ee1"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto :goto_1

    :cond_3
    invoke-virtual {p0}, Lpmsj/work/e/au;->af()I

    move-result v1

    if-ne v1, v8, :cond_4

    const/16 v1, 0x3f1

    const/16 v2, 0x2f

    iget v0, v0, Lpmsj/work/b/j;->e:I

    invoke-static {v1, v2, v0}, Lpmsj/work/main/w;->a(ISI)V

    goto :goto_1

    :cond_4
    const/16 v1, 0x3f1

    const/16 v2, 0x1d

    iget v0, v0, Lpmsj/work/b/j;->e:I

    invoke-static {}, Lpmsj/work/b/m;->d()Lpmsj/work/b/m;

    move-result-object v3

    invoke-virtual {v3}, Lpmsj/work/b/m;->h()I

    move-result v3

    invoke-static {v1, v2, v0, v3}, Lpmsj/work/main/w;->a(ISII)V

    goto :goto_1

    :cond_5
    const-string v1, "\u4ea4\u6613"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_6

    const-string v1, "\u5356\u51fa"

    invoke-virtual {p1, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_6

    const-string v1, "\u8d60\u9001"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_6

    const-string v1, "\u5bc4\u552e"

    invoke-virtual {p1, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_6

    const-string v1, "\u6446\u644a"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_1a

    :cond_6
    const/16 v1, 0x33

    iget-byte v2, v0, Lpmsj/work/b/j;->k:B

    if-ne v1, v2, :cond_7

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "\u4efb\u52a1\u7269\u54c1\u4e0d\u5141\u8bb8"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v8

    goto/16 :goto_0

    :cond_7
    invoke-virtual {v0, v8}, Lpmsj/work/b/j;->e(I)Z

    move-result v1

    if-eqz v1, :cond_8

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "\u6b64\u7269\u54c1\u4e3a\u8d60\u54c1,\u4e0d\u5141\u8bb8"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v8

    goto/16 :goto_0

    :cond_8
    const/4 v1, 0x4

    invoke-virtual {v0, v1}, Lpmsj/work/b/j;->e(I)Z

    move-result v1

    if-eqz v1, :cond_9

    const-string v1, "\u5356\u51fa"

    invoke-virtual {p1, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_9

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "\u7ed1\u5b9a\u4e2d\uff0c\u4e0d\u5141\u8bb8"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v8

    goto/16 :goto_0

    :cond_9
    const-string v1, "\u5356\u51fa"

    invoke-virtual {p1, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-nez v1, :cond_a

    invoke-virtual {v0, v4}, Lpmsj/work/b/j;->d(I)Z

    move-result v1

    if-eqz v1, :cond_a

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "\u6b64\u7269\u54c1\u4e0d\u5141\u8bb8"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v8

    goto/16 :goto_0

    :cond_a
    const/16 v1, 0x8

    invoke-virtual {v0, v1}, Lpmsj/work/b/j;->e(I)Z

    move-result v1

    if-eqz v1, :cond_b

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    new-instance v1, Ljava/lang/StringBuilder;

    invoke-direct {v1}, Ljava/lang/StringBuilder;-><init>()V

    const-string v2, "\u5df2\u6fc0\u6d3b\u7684\u7269\u54c1\u4e0d\u53ef"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1, p1}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    move v0, v8

    goto/16 :goto_0

    :cond_b
    const-string v1, "\u4ea4\u6613"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_d

    invoke-direct {p0, v0}, Lpmsj/work/e/au;->e(Lpmsj/work/b/j;)V

    :cond_c
    :goto_2
    move v0, v8

    goto/16 :goto_0

    :cond_d
    const-string v1, "\u5356\u51fa"

    invoke-virtual {p1, v5}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_10

    invoke-virtual {v0, v8}, Lpmsj/work/b/j;->d(I)Z

    move-result v1

    if-eqz v1, :cond_e

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    const-string v1, "\u8be5\u7269\u54c1\u4e0d\u5141\u8bb8\u5356\u51fa"

    invoke-virtual {v0, v1}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto :goto_2

    :cond_e
    const/4 v1, 0x4

    invoke-virtual {v0, v1}, Lpmsj/work/b/j;->d(I)Z

    move-result v1

    if-eqz v1, :cond_f

    new-instance v1, Ljava/lang/StringBuffer;

    const-string v2, "*"

    invoke-direct {v1, v2}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    sget-byte v2, Lpmsj/work/a/c;->n:B

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    iget-object v2, v0, Lpmsj/work/b/j;->o:Ljava/lang/String;

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v2, "*0"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v2, "\u4e3a\u8d35\u91cd\u7269\u54c1\uff0c"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v2, "\u786e\u5b9a\u5356\u51fa\uff1f"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v1, v4}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    const-string v2, "\u5356\u51fa\u4ef7\u683c:"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v2, "*"

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    sget-byte v2, Lpmsj/work/a/c;->o:B

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Lpmsj/work/b/j;->s()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    const/16 v2, 0xb

    invoke-virtual {v0, v1, v2, p0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    goto :goto_2

    :cond_f
    invoke-static {v0}, Lpmsj/work/e/au;->c(Lpmsj/work/b/j;)V

    goto :goto_2

    :cond_10
    const-string v1, "\u8d60\u9001"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_12

    const/4 v1, 0x4

    invoke-virtual {v0, v1}, Lpmsj/work/b/j;->d(I)Z

    move-result v1

    if-eqz v1, :cond_11

    new-instance v1, Ljava/lang/StringBuffer;

    const-string v2, "*"

    invoke-direct {v1, v2}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    sget-byte v2, Lpmsj/work/a/c;->n:B

    invoke-virtual {v1, v2}, Ljava/lang/StringBuffer;->append(I)Ljava/lang/StringBuffer;

    iget-object v0, v0, Lpmsj/work/b/j;->o:Ljava/lang/String;

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "*0"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "\u4e3a\u8d35\u91cd\u7269\u54c1\uff0c"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "\u786e\u5b9a\u9001\u51fa?"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    const/16 v2, 0xc

    invoke-virtual {v0, v1, v2, p0}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;)Lpmsj/work/e/aa;

    goto/16 :goto_2

    :cond_11
    invoke-direct {p0, v0}, Lpmsj/work/e/au;->e(Lpmsj/work/b/j;)V

    goto/16 :goto_2

    :cond_12
    const-string v1, "\u5bc4\u552e"

    invoke-virtual {p1, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_16

    iget v1, p0, Lpmsj/work/e/au;->ab:I

    if-nez v1, :cond_14

    const-string v0, "\u5bc4\u552e"

    invoke-virtual {p1, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_13

    const-string v0, "\u5bc4\u552e\u7269\u603b\u6570\u5df2\u5230\u4e0a\u9650"

    :goto_3
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto/16 :goto_2

    :cond_13
    const-string v0, "\u6446\u644a\u7269\u603b\u6570\u5df2\u5230\u4e0a\u9650"

    goto :goto_3

    :cond_14
    const-string v1, "\u5bc4\u552e"

    invoke-virtual {p1, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_15

    const/16 v1, 0xd

    move v2, v1

    :goto_4
    new-instance v1, Ljava/lang/StringBuffer;

    const-string v3, "\u8bf7\u8f93\u5165"

    invoke-direct {v1, v3}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v4}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Lpmsj/work/b/j;->q()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v1, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Lpmsj/work/b/j;->r()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    const-string v0, "\u7684\u552e\u4ef7"

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    const/16 v4, 0x9

    const-string v5, "\u8bf7\u8f93\u5165\u552e\u4ef7"

    const-string v7, ""

    move-object v3, p0

    invoke-virtual/range {v0 .. v7}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;ILjava/lang/String;ILjava/lang/String;)Lpmsj/work/d/c;

    goto/16 :goto_2

    :cond_15
    const/16 v1, 0xe

    move v2, v1

    goto :goto_4

    :cond_16
    const-string v1, "\u6446\u644a"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_c

    iget v1, p0, Lpmsj/work/e/au;->ab:I

    if-nez v1, :cond_18

    const-string v0, "\u5bc4\u552e"

    invoke-virtual {p1, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_17

    const-string v0, "\u5bc4\u552e\u7269\u603b\u6570\u5df2\u5230\u4e0a\u9650"

    :goto_5
    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v1

    invoke-virtual {v1, v0}, Lpmsj/work/d/n;->a(Ljava/lang/String;)Lpmsj/work/e/br;

    goto/16 :goto_2

    :cond_17
    const-string v0, "\u6446\u644a\u7269\u603b\u6570\u5df2\u5230\u4e0a\u9650"

    goto :goto_5

    :cond_18
    const-string v1, "\u5bc4\u552e"

    invoke-virtual {p1, v3}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_19

    const/16 v1, 0xd

    move v2, v1

    :goto_6
    new-instance v1, Ljava/lang/StringBuffer;

    const-string v3, "\u8bf7\u8f93\u5165\u552e\u4ef7"

    invoke-direct {v1, v3}, Ljava/lang/StringBuffer;-><init>(Ljava/lang/String;)V

    invoke-virtual {v1, v4}, Ljava/lang/StringBuffer;->append(C)Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Lpmsj/work/b/j;->q()Ljava/lang/String;

    move-result-object v3

    invoke-virtual {v1, v3}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-virtual {v0}, Lpmsj/work/b/j;->r()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v1, v0}, Ljava/lang/StringBuffer;->append(Ljava/lang/String;)Ljava/lang/StringBuffer;

    invoke-static {}, Lpmsj/work/d/n;->f()Lpmsj/work/d/n;

    move-result-object v0

    invoke-virtual {v1}, Ljava/lang/StringBuffer;->toString()Ljava/lang/String;

    move-result-object v1

    const/16 v4, 0x9

    const-string v5, "\u8bf7\u8f93\u5165\u552e\u4ef7"

    const-string v7, ""

    move-object v3, p0

    invoke-virtual/range {v0 .. v7}, Lpmsj/work/d/n;->a(Ljava/lang/String;ILpmsj/work/d/c;ILjava/lang/String;ILjava/lang/String;)Lpmsj/work/d/c;

    goto/16 :goto_2

    :cond_19
    const/16 v1, 0xe

    move v2, v1

    goto :goto_6

    :cond_1a
    const-string v1, "\u4f7f\u7528\u7269\u54c1:"

    invoke-virtual {p1, v1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v1

    if-eqz v1, :cond_c

    invoke-static {v0}, Lpmsj/work/main/c;->a(Lpmsj/work/b/j;)V

    goto/16 :goto_2
.end method

.method protected final c()V
    .locals 2

    invoke-super {p0}, Lpmsj/work/e/at;->c()V

    const/16 v0, 0x138a

    invoke-virtual {p0, v0}, Lpmsj/work/e/au;->w(I)Lpmsj/work/d/b;

    move-result-object v0

    const/4 v1, 0x1

    invoke-virtual {v0, v1}, Lpmsj/work/d/b;->l(I)V

    return-void
.end method

.method public final c_(I)V
    .locals 1

    invoke-super {p0, p1}, Lpmsj/work/e/at;->c_(I)V

    packed-switch p1, :pswitch_data_0

    :goto_0
    return-void

    :pswitch_0
    invoke-virtual {p0}, Lpmsj/work/e/au;->i()Lpmsj/work/b/j;

    move-result-object v0

    invoke-static {v0}, Lpmsj/work/e/au;->c(Lpmsj/work/b/j;)V

    goto :goto_0

    :pswitch_1
    invoke-virtual {p0}, Lpmsj/work/e/au;->i()Lpmsj/work/b/j;

    move-result-object v0

    invoke-direct {p0, v0}, Lpmsj/work/e/au;->e(Lpmsj/work/b/j;)V

    goto :goto_0

    nop

    :pswitch_data_0
    .packed-switch 0xb
        :pswitch_0
        :pswitch_1
    .end packed-switch
.end method

.method protected final g()V
    .locals 2

    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    if-eqz v0, :cond_0

    iget-object v0, p0, Lpmsj/work/e/au;->r:Lpmsj/work/d/c;

    iget-object v1, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    invoke-virtual {v0, v1}, Lpmsj/work/d/c;->a(Ljava/util/Vector;)Z

    invoke-virtual {p0}, Lpmsj/work/e/au;->ae()V

    :goto_0
    return-void

    :cond_0
    invoke-super {p0}, Lpmsj/work/e/at;->g()V

    goto :goto_0
.end method

.method public final g(Ljava/lang/String;)V
    .locals 1

    const/16 v0, 0x400

    iput v0, p0, Lpmsj/work/e/au;->ak:I

    const/16 v0, 0x28

    iput-byte v0, p0, Lpmsj/work/e/au;->al:B

    if-eqz p1, :cond_0

    const-string v0, ""

    invoke-virtual {v0, p1}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    invoke-virtual {p0, p1}, Lpmsj/work/e/au;->e(Ljava/lang/String;)V

    goto :goto_0
.end method

.method protected final l()Z
    .locals 3

    const/4 v2, 0x1

    invoke-virtual {p0}, Lpmsj/work/e/au;->at()Z

    move-result v0

    if-nez v0, :cond_0

    iget v0, p0, Lpmsj/work/e/au;->ak:I

    if-lez v0, :cond_0

    const/4 v0, 0x0

    invoke-static {v0, v2}, Lpmsj/work/main/t;->a(ZZ)V

    iget v0, p0, Lpmsj/work/e/au;->ak:I

    iget-byte v1, p0, Lpmsj/work/e/au;->al:B

    invoke-static {v0, v1}, Lpmsj/work/main/w;->a(IB)V

    invoke-virtual {p0}, Lpmsj/work/e/au;->ae()V

    move v0, v2

    :goto_0
    return v0

    :cond_0
    invoke-super {p0}, Lpmsj/work/e/at;->l()Z

    move-result v0

    goto :goto_0
.end method

.method protected final o()V
    .locals 8

    const/4 v7, 0x0

    iget-boolean v0, p0, Lpmsj/work/e/au;->ad:Z

    if-eqz v0, :cond_0

    invoke-virtual {p0}, Lpmsj/work/e/au;->j()Ljava/util/Vector;

    move-result-object v1

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v2

    move v3, v7

    :goto_0
    if-ge v3, v2, :cond_4

    invoke-virtual {v1, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/j;

    iget-object v4, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0}, Lpmsj/work/b/j;->q()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v0}, Lpmsj/work/b/j;->r()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    iget-object v4, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    invoke-virtual {v0}, Lpmsj/work/b/j;->s()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {v4, v0}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_0

    :cond_0
    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    if-eqz v0, :cond_3

    iget-object v0, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    invoke-virtual {v0}, Ljava/util/Vector;->size()I

    move-result v0

    if-lez v0, :cond_3

    invoke-virtual {p0}, Lpmsj/work/e/au;->j()Ljava/util/Vector;

    move-result-object v1

    invoke-virtual {v1}, Ljava/util/Vector;->size()I

    move-result v2

    move v3, v7

    :goto_1
    if-ge v3, v2, :cond_4

    invoke-virtual {v1, v3}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v0

    check-cast v0, Lpmsj/work/b/j;

    iget-object v4, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    new-instance v5, Ljava/lang/StringBuilder;

    invoke-direct {v5}, Ljava/lang/StringBuilder;-><init>()V

    invoke-virtual {v0}, Lpmsj/work/b/j;->q()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v0}, Lpmsj/work/b/j;->r()Ljava/lang/String;

    move-result-object v6

    invoke-virtual {v5, v6}, Ljava/lang/StringBuilder;->append(Ljava/lang/String;)Ljava/lang/StringBuilder;

    move-result-object v5

    invoke-virtual {v5}, Ljava/lang/StringBuilder;->toString()Ljava/lang/String;

    move-result-object v5

    invoke-virtual {v4, v5}, Lpmsj/work/d/l;->i(Ljava/lang/String;)Z

    move v4, v7

    :goto_2
    iget-object v5, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    invoke-virtual {v5}, Ljava/util/Vector;->size()I

    move-result v5

    if-ge v4, v5, :cond_1

    iget-object v5, p0, Lpmsj/work/e/au;->aa:Ljava/util/Vector;

    invoke-virtual {v5, v4}, Ljava/util/Vector;->elementAt(I)Ljava/lang/Object;

    move-result-object v5

    if-ne v0, v5, :cond_2

    const/16 v0, 0x26ac

    invoke-static {v7, v0, v7, v7}, Lpmsj/work/a/k;->a(IIII)Ljava/lang/String;

    move-result-object v0

    iget-object v4, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    invoke-virtual {v4, v0}, Lpmsj/work/d/l;->g(Ljava/lang/String;)V

    :cond_1
    add-int/lit8 v0, v3, 0x1

    move v3, v0

    goto :goto_1

    :cond_2
    add-int/lit8 v4, v4, 0x1

    goto :goto_2

    :cond_3
    invoke-super {p0}, Lpmsj/work/e/at;->o()V

    :cond_4
    return-void
.end method

.method protected final r()V
    .locals 5

    const/4 v4, 0x0

    invoke-virtual {p0}, Lpmsj/work/e/au;->i()Lpmsj/work/b/j;

    move-result-object v0

    if-eqz v0, :cond_3

    invoke-virtual {v0}, Lpmsj/work/b/j;->c()Z

    move-result v1

    if-eqz v1, :cond_3

    iget-object v1, p0, Lpmsj/work/e/au;->ac:Lpmsj/work/b/g;

    if-eqz v1, :cond_3

    const/4 v1, 0x1

    iget-object v2, p0, Lpmsj/work/e/au;->c:Lpmsj/work/d/l;

    invoke-virtual {v2}, Lpmsj/work/d/l;->f()I

    move-result v2

    if-ne v1, v2, :cond_3

    iget-object v1, p0, Lpmsj/work/e/au;->c:Lpmsj/work/d/l;

    invoke-virtual {v1}, Lpmsj/work/d/l;->k()V

    check-cast v0, Lpmsj/work/b/g;

    move v1, v4

    :goto_0
    const/16 v2, 0x8

    if-ge v1, v2, :cond_1

    invoke-virtual {v0, v1}, Lpmsj/work/b/g;->a(B)I

    move-result v2

    iget-object v3, p0, Lpmsj/work/e/au;->ac:Lpmsj/work/b/g;

    invoke-virtual {v3, v1}, Lpmsj/work/b/g;->a(B)I

    move-result v3

    sub-int/2addr v2, v3

    if-eqz v2, :cond_0

    sget-object v3, Lpmsj/work/a/c;->ax:[Ljava/lang/String;

    aget-object v3, v3, v1

    invoke-direct {p0, v3, v2}, Lpmsj/work/e/au;->b(Ljava/lang/String;I)V

    :cond_0
    add-int/lit8 v1, v1, 0x1

    int-to-byte v1, v1

    goto :goto_0

    :cond_1
    move v1, v4

    :goto_1
    const/4 v2, 0x5

    if-ge v1, v2, :cond_4

    invoke-virtual {v0, v1}, Lpmsj/work/b/g;->d(B)I

    move-result v2

    iget-object v3, p0, Lpmsj/work/e/au;->ac:Lpmsj/work/b/g;

    invoke-virtual {v3, v1}, Lpmsj/work/b/g;->d(B)I

    move-result v3

    sub-int/2addr v2, v3

    if-eqz v2, :cond_2

    sget-object v3, Lpmsj/work/a/c;->au:[Ljava/lang/String;

    aget-object v3, v3, v1

    invoke-direct {p0, v3, v2}, Lpmsj/work/e/au;->b(Ljava/lang/String;I)V

    :cond_2
    add-int/lit8 v1, v1, 0x1

    int-to-byte v1, v1

    goto :goto_1

    :cond_3
    invoke-super {p0}, Lpmsj/work/e/at;->r()V

    :cond_4
    return-void
.end method

.method protected final s()V
    .locals 4

    const/16 v3, 0x24

    const/4 v2, 0x6

    iget-object v0, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    iget-object v1, p0, Lpmsj/work/e/au;->d:Lpmsj/work/d/k;

    iget-short v1, v1, Lpmsj/work/d/b;->j:S

    add-int/lit8 v1, v1, 0x24

    sub-int/2addr v1, v2

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->j:S

    iget-object v0, p0, Lpmsj/work/e/au;->W:Lpmsj/work/d/g;

    iget-object v1, p0, Lpmsj/work/e/au;->W:Lpmsj/work/d/g;

    iget-short v1, v1, Lpmsj/work/d/b;->j:S

    add-int/lit8 v1, v1, 0x24

    sub-int/2addr v1, v2

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->j:S

    iget-object v0, p0, Lpmsj/work/e/au;->X:Lpmsj/work/d/l;

    iget-object v1, p0, Lpmsj/work/e/au;->X:Lpmsj/work/d/l;

    iget-short v1, v1, Lpmsj/work/d/b;->j:S

    add-int/lit8 v1, v1, 0x24

    sub-int/2addr v1, v2

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->j:S

    iget-object v0, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    iget-object v1, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    iget-short v1, v1, Lpmsj/work/d/b;->j:S

    add-int/lit8 v1, v1, 0x24

    sub-int/2addr v1, v2

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->j:S

    iget-object v0, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    iget-object v1, p0, Lpmsj/work/e/au;->a:Lpmsj/work/d/l;

    iget v1, v1, Lpmsj/work/d/b;->l:I

    sub-int/2addr v1, v3

    add-int/lit8 v1, v1, 0x6

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->j(I)V

    iget-object v0, p0, Lpmsj/work/e/au;->b:Lpmsj/work/d/l;

    iget-object v1, p0, Lpmsj/work/e/au;->b:Lpmsj/work/d/l;

    iget-short v1, v1, Lpmsj/work/d/b;->j:S

    add-int/lit8 v1, v1, 0x24

    sub-int/2addr v1, v2

    int-to-short v1, v1

    iput-short v1, v0, Lpmsj/work/d/b;->j:S

    iget-object v0, p0, Lpmsj/work/e/au;->b:Lpmsj/work/d/l;

    iget-object v1, p0, Lpmsj/work/e/au;->b:Lpmsj/work/d/l;

    iget v1, v1, Lpmsj/work/d/b;->l:I

    sub-int/2addr v1, v3

    add-int/lit8 v1, v1, 0x6

    invoke-virtual {v0, v1}, Lpmsj/work/d/l;->j(I)V

    invoke-virtual {p0, v3}, Lpmsj/work/e/au;->z(I)V

    return-void
.end method
