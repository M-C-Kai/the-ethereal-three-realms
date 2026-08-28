.class public final Lpmsj/work/d/a;
.super Lpmsj/work/d/b;


# instance fields
.field private A:I

.field private B:I

.field private C:I

.field private D:I

.field private E:[I

.field private F:I

.field private G:I

.field private H:I

.field private I:I

.field private J:I

.field private K:I

.field private L:I

.field private M:Lpmsj/work/a/i;

.field private N:B

.field private O:Lpmsj/work/a/i;

.field private P:Lpmsj/work/a/i;

.field private Q:Lpmsj/work/a/i;

.field private R:Lpmsj/work/a/i;

.field private S:I

.field private T:Lpmsj/work/a/i;

.field a:I

.field b:I

.field private c:Ljava/lang/String;

.field private d:I

.field private e:I

.field private f:I

.field private r:Lpmsj/work/a/i;

.field private s:B

.field private t:Lpmsj/work/a/i;

.field private u:La/a/d;

.field private v:Z

.field private w:La/c/q;

.field private x:Lpmsj/work/a/i;

.field private y:B

.field private z:Lpmsj/work/d/e;


# direct methods
.method public constructor <init>(ILa/c/l;)V
    .locals 4

    const/4 v2, -0x1

    const/4 v1, 0x0

    const/4 v3, 0x0

    invoke-direct {p0, v3, v3}, Lpmsj/work/d/b;-><init>(II)V

    iput-byte v3, p0, Lpmsj/work/d/a;->s:B

    new-instance v0, La/c/q;

    invoke-direct {v0}, La/c/q;-><init>()V

    iput-object v0, p0, Lpmsj/work/d/a;->w:La/c/q;

    iput-byte v3, p0, Lpmsj/work/d/a;->y:B

    iput v2, p0, Lpmsj/work/d/a;->A:I

    const/4 v0, 0x3

    iput v0, p0, Lpmsj/work/d/a;->B:I

    iput v3, p0, Lpmsj/work/d/a;->C:I

    iput v3, p0, Lpmsj/work/d/a;->D:I

    iput v2, p0, Lpmsj/work/d/a;->F:I

    iget-short v0, p0, Lpmsj/work/d/a;->i:S

    iput v0, p0, Lpmsj/work/d/a;->G:I

    iget-short v0, p0, Lpmsj/work/d/a;->j:S

    iput v0, p0, Lpmsj/work/d/a;->H:I

    iget v0, p0, Lpmsj/work/d/a;->k:I

    iput v0, p0, Lpmsj/work/d/a;->I:I

    iget v0, p0, Lpmsj/work/d/a;->l:I

    iput v0, p0, Lpmsj/work/d/a;->J:I

    const/4 v0, 0x7

    iput v0, p0, Lpmsj/work/d/a;->K:I

    sget v0, La/c/x;->a:I

    iput v0, p0, Lpmsj/work/d/a;->L:I

    iput-object v1, p0, Lpmsj/work/d/a;->M:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->R:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->T:Lpmsj/work/a/i;

    const/high16 v0, 0x800000

    invoke-virtual {p0, v0}, Lpmsj/work/d/a;->l(I)V

    invoke-virtual {p0, p1, p2}, Lpmsj/work/d/a;->a(ILa/c/l;)V

    invoke-virtual {p2}, La/c/l;->c()Ljava/lang/String;

    move-result-object v0

    invoke-virtual {p0, v0}, Lpmsj/work/d/a;->a_(Ljava/lang/String;)V

    invoke-virtual {p2}, La/c/l;->b()I

    move-result v0

    invoke-virtual {p2}, La/c/l;->read()I

    move-result v1

    int-to-byte v1, v1

    if-lez v0, :cond_0

    new-instance v2, Lpmsj/work/a/i;

    invoke-direct {v2, v0, v1}, Lpmsj/work/a/i;-><init>(II)V

    invoke-virtual {p0, v2, v3}, Lpmsj/work/d/a;->a(Lpmsj/work/a/i;B)V

    :cond_0
    invoke-virtual {p2}, La/c/l;->read()I

    return-void
.end method

.method public constructor <init>(Ljava/lang/String;I)V
    .locals 4

    const/4 v3, -0x1

    const/4 v2, 0x0

    const/4 v1, 0x0

    invoke-direct {p0, v1, v1}, Lpmsj/work/d/b;-><init>(II)V

    iput-byte v1, p0, Lpmsj/work/d/a;->s:B

    new-instance v0, La/c/q;

    invoke-direct {v0}, La/c/q;-><init>()V

    iput-object v0, p0, Lpmsj/work/d/a;->w:La/c/q;

    iput-byte v1, p0, Lpmsj/work/d/a;->y:B

    iput v3, p0, Lpmsj/work/d/a;->A:I

    const/4 v0, 0x3

    iput v0, p0, Lpmsj/work/d/a;->B:I

    iput v1, p0, Lpmsj/work/d/a;->C:I

    iput v1, p0, Lpmsj/work/d/a;->D:I

    iput v3, p0, Lpmsj/work/d/a;->F:I

    iget-short v0, p0, Lpmsj/work/d/a;->i:S

    iput v0, p0, Lpmsj/work/d/a;->G:I

    iget-short v0, p0, Lpmsj/work/d/a;->j:S

    iput v0, p0, Lpmsj/work/d/a;->H:I

    iget v0, p0, Lpmsj/work/d/a;->k:I

    iput v0, p0, Lpmsj/work/d/a;->I:I

    iget v0, p0, Lpmsj/work/d/a;->l:I

    iput v0, p0, Lpmsj/work/d/a;->J:I

    const/4 v0, 0x7

    iput v0, p0, Lpmsj/work/d/a;->K:I

    sget v0, La/c/x;->a:I

    iput v0, p0, Lpmsj/work/d/a;->L:I

    iput-object v2, p0, Lpmsj/work/d/a;->M:Lpmsj/work/a/i;

    iput-object v2, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    iput-object v2, p0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    iput-object v2, p0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    iput-object v2, p0, Lpmsj/work/d/a;->R:Lpmsj/work/a/i;

    iput-object v2, p0, Lpmsj/work/d/a;->T:Lpmsj/work/a/i;

    const/high16 v0, 0x800000

    invoke-virtual {p0, v0}, Lpmsj/work/d/a;->l(I)V

    iput-object p1, p0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    iput p2, p0, Lpmsj/work/d/a;->m:I

    sget-object v0, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v0, p1}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v0

    iput v0, p0, Lpmsj/work/d/a;->k:I

    sget-object v0, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v0, p1}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v0

    iput v0, p0, Lpmsj/work/d/a;->d:I

    return-void
.end method

.method public constructor <init>(Ljava/lang/String;II)V
    .locals 4

    const/4 v3, -0x1

    const/4 v2, 0x0

    const/4 v1, 0x0

    invoke-direct {p0, p2, p3}, Lpmsj/work/d/b;-><init>(II)V

    iput-byte v2, p0, Lpmsj/work/d/a;->s:B

    new-instance v0, La/c/q;

    invoke-direct {v0}, La/c/q;-><init>()V

    iput-object v0, p0, Lpmsj/work/d/a;->w:La/c/q;

    iput-byte v2, p0, Lpmsj/work/d/a;->y:B

    iput v3, p0, Lpmsj/work/d/a;->A:I

    const/4 v0, 0x3

    iput v0, p0, Lpmsj/work/d/a;->B:I

    iput v2, p0, Lpmsj/work/d/a;->C:I

    iput v2, p0, Lpmsj/work/d/a;->D:I

    iput v3, p0, Lpmsj/work/d/a;->F:I

    iget-short v0, p0, Lpmsj/work/d/a;->i:S

    iput v0, p0, Lpmsj/work/d/a;->G:I

    iget-short v0, p0, Lpmsj/work/d/a;->j:S

    iput v0, p0, Lpmsj/work/d/a;->H:I

    iget v0, p0, Lpmsj/work/d/a;->k:I

    iput v0, p0, Lpmsj/work/d/a;->I:I

    iget v0, p0, Lpmsj/work/d/a;->l:I

    iput v0, p0, Lpmsj/work/d/a;->J:I

    const/4 v0, 0x7

    iput v0, p0, Lpmsj/work/d/a;->K:I

    sget v0, La/c/x;->a:I

    iput v0, p0, Lpmsj/work/d/a;->L:I

    iput-object v1, p0, Lpmsj/work/d/a;->M:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->R:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->T:Lpmsj/work/a/i;

    const/high16 v0, 0x800000

    invoke-virtual {p0, v0}, Lpmsj/work/d/a;->l(I)V

    iput-object p1, p0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    if-nez p2, :cond_0

    sget-object v0, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v0, p1}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v0

    iput v0, p0, Lpmsj/work/d/a;->k:I

    :cond_0
    sget-object v0, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v0, p1}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v0

    iput v0, p0, Lpmsj/work/d/a;->d:I

    return-void
.end method


# virtual methods
.method public final a(I)V
    .locals 0

    iput p1, p0, Lpmsj/work/d/a;->L:I

    return-void
.end method

.method public final a(II)V
    .locals 0

    iput p1, p0, Lpmsj/work/d/a;->C:I

    iput p2, p0, Lpmsj/work/d/a;->D:I

    return-void
.end method

.method public final a(IIII)V
    .locals 1

    if-ltz p1, :cond_0

    iput p1, p0, Lpmsj/work/d/a;->G:I

    :cond_0
    if-ltz p2, :cond_1

    iput p2, p0, Lpmsj/work/d/a;->H:I

    :cond_1
    if-ltz p3, :cond_2

    iput p3, p0, Lpmsj/work/d/a;->I:I

    :cond_2
    if-ltz p4, :cond_3

    iput p4, p0, Lpmsj/work/d/a;->J:I

    :cond_3
    const/4 v0, 0x7

    iput v0, p0, Lpmsj/work/d/a;->K:I

    return-void
.end method

.method public final a(La/a/d;)V
    .locals 0

    iput-object p1, p0, Lpmsj/work/d/a;->u:La/a/d;

    return-void
.end method

.method public final a(Ljava/lang/String;II)V
    .locals 4

    iput-object p1, p0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    iput p2, p0, Lpmsj/work/d/a;->A:I

    iput p3, p0, Lpmsj/work/d/a;->B:I

    new-instance v0, Lpmsj/work/d/e;

    iget-object v1, p0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    iget v2, p0, Lpmsj/work/d/a;->A:I

    iget v3, p0, Lpmsj/work/d/a;->B:I

    invoke-direct {v0, v1, v2, v3}, Lpmsj/work/d/e;-><init>(Ljava/lang/String;II)V

    invoke-virtual {v0}, Lpmsj/work/d/e;->a()I

    move-result v1

    iget v2, p0, Lpmsj/work/d/a;->k:I

    if-le v1, v2, :cond_0

    invoke-virtual {v0}, Lpmsj/work/d/e;->a()I

    move-result v1

    :goto_0
    iput v1, p0, Lpmsj/work/d/a;->k:I

    invoke-virtual {v0}, Lpmsj/work/d/e;->b()I

    move-result v1

    iget v2, p0, Lpmsj/work/d/a;->l:I

    if-le v1, v2, :cond_1

    invoke-virtual {v0}, Lpmsj/work/d/e;->b()I

    move-result v1

    :goto_1
    iput v1, p0, Lpmsj/work/d/a;->l:I

    iput-object v0, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    return-void

    :cond_0
    iget v1, p0, Lpmsj/work/d/a;->k:I

    goto :goto_0

    :cond_1
    iget v1, p0, Lpmsj/work/d/a;->l:I

    goto :goto_1
.end method

.method public final a(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 5

    iget v0, p0, Lpmsj/work/d/a;->h:I

    const/high16 v1, 0x400000

    and-int/2addr v0, v1

    if-eqz v0, :cond_2

    iget v0, p0, Lpmsj/work/d/a;->k:I

    add-int/2addr v0, p2

    iget-object v1, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    invoke-virtual {v1}, Lpmsj/work/d/e;->a()I

    move-result v1

    sub-int/2addr v0, v1

    const/4 v1, 0x2

    sub-int/2addr v0, v1

    iget v1, p0, Lpmsj/work/d/a;->l:I

    iget-object v2, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    invoke-virtual {v2}, Lpmsj/work/d/e;->b()I

    move-result v2

    sub-int/2addr v1, v2

    shr-int/lit8 v1, v1, 0x1

    add-int/2addr v1, p3

    move v4, v1

    move v1, v0

    move v0, v4

    :goto_0
    iget v2, p0, Lpmsj/work/d/a;->C:I

    add-int/2addr v1, v2

    iget v2, p0, Lpmsj/work/d/a;->D:I

    add-int/2addr v0, v2

    iget-object v2, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    if-eqz v2, :cond_1

    iget v2, p0, Lpmsj/work/d/a;->B:I

    const/4 v3, -0x1

    if-eq v2, v3, :cond_0

    iget-object v2, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    iget v3, p0, Lpmsj/work/d/a;->B:I

    invoke-virtual {v2, v3}, Lpmsj/work/d/e;->a(I)V

    :cond_0
    iget-object v2, p0, Lpmsj/work/d/a;->E:[I

    if-eqz v2, :cond_3

    iget-object v2, p0, Lpmsj/work/d/a;->E:[I

    array-length v2, v2

    iget-object v3, p0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    invoke-virtual {v3}, Ljava/lang/String;->length()I

    move-result v3

    if-ne v2, v3, :cond_3

    iget-object v2, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    iget-object v3, p0, Lpmsj/work/d/a;->E:[I

    invoke-virtual {v2, p1, v1, v0, v3}, Lpmsj/work/d/e;->a(Ljavax/microedition/lcdui/Graphics;II[I)V

    :cond_1
    :goto_1
    return-void

    :cond_2
    iget v0, p0, Lpmsj/work/d/a;->h:I

    const/high16 v1, 0x800000

    and-int/2addr v0, v1

    if-eqz v0, :cond_4

    iget v0, p0, Lpmsj/work/d/a;->k:I

    iget-object v1, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    invoke-virtual {v1}, Lpmsj/work/d/e;->a()I

    move-result v1

    sub-int/2addr v0, v1

    if-lez v0, :cond_4

    iget v0, p0, Lpmsj/work/d/a;->k:I

    iget-object v1, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    invoke-virtual {v1}, Lpmsj/work/d/e;->a()I

    move-result v1

    sub-int/2addr v0, v1

    shr-int/lit8 v0, v0, 0x1

    add-int/2addr v0, p2

    iget v1, p0, Lpmsj/work/d/a;->l:I

    iget-object v2, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    invoke-virtual {v2}, Lpmsj/work/d/e;->b()I

    move-result v2

    sub-int/2addr v1, v2

    shr-int/lit8 v1, v1, 0x1

    add-int/2addr v1, p3

    move v4, v1

    move v1, v0

    move v0, v4

    goto :goto_0

    :cond_3
    iget-object v2, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    invoke-virtual {v2, p1, v1, v0}, Lpmsj/work/d/e;->a(Ljavax/microedition/lcdui/Graphics;II)V

    goto :goto_1

    :cond_4
    move v0, p3

    move v1, p2

    goto :goto_0
.end method

.method public final a(Ljavax/microedition/lcdui/Graphics;IIIIB)V
    .locals 7

    const/4 v5, 0x0

    iget-object v0, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    if-nez v0, :cond_0

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x147790

    invoke-direct {v0, v1, v5}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    :cond_0
    iget-object v0, p0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    if-nez v0, :cond_1

    new-instance v0, Lpmsj/work/a/i;

    const v1, 0x147664

    invoke-direct {v0, v1, v5}, Lpmsj/work/a/i;-><init>(II)V

    iput-object v0, p0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    :cond_1
    iget-object v0, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    invoke-virtual {v0}, Lpmsj/work/a/i;->b()I

    move-result v0

    sub-int v0, p5, v0

    if-lez v0, :cond_4

    iget-object v0, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    invoke-virtual {v0}, Lpmsj/work/a/i;->b()I

    move-result v0

    sub-int v0, p5, v0

    div-int/lit8 v0, v0, 0x2

    add-int/2addr v0, p3

    move v3, v0

    :goto_0
    iget-object v0, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    invoke-virtual {v0}, Lpmsj/work/a/i;->c()I

    move-result v0

    if-ge p4, v0, :cond_2

    :goto_1
    return-void

    :cond_2
    iget-object v0, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    move-object v1, p1

    move v2, p2

    move v4, p6

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    iget-object v0, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    invoke-virtual {v0}, Lpmsj/work/a/i;->c()I

    move-result v0

    mul-int/lit8 v0, v0, 0x2

    if-le p4, v0, :cond_3

    iget-object v1, p0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    iget-object v0, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    invoke-virtual {v0}, Lpmsj/work/a/i;->c()I

    move-result v0

    add-int v2, p2, v0

    iget-object v0, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    invoke-virtual {v0}, Lpmsj/work/a/i;->c()I

    move-result v0

    mul-int/lit8 v0, v0, 0x2

    sub-int v4, p4, v0

    move v5, p6

    move-object v6, p1

    invoke-virtual/range {v1 .. v6}, Lpmsj/work/a/i;->a(IIIILjavax/microedition/lcdui/Graphics;)V

    :cond_3
    iget-object v0, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    add-int v1, p2, p4

    iget-object v2, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    invoke-virtual {v2}, Lpmsj/work/a/i;->c()I

    move-result v2

    sub-int v2, v1, v2

    const/4 v5, 0x2

    move-object v1, p1

    move v4, p6

    invoke-virtual/range {v0 .. v5}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    goto :goto_1

    :cond_4
    move v3, p3

    goto :goto_0
.end method

.method public final a(Lpmsj/work/a/i;)V
    .locals 0

    iput-object p1, p0, Lpmsj/work/d/a;->t:Lpmsj/work/a/i;

    return-void
.end method

.method public final a(Lpmsj/work/a/i;B)V
    .locals 1

    iput-object p1, p0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    iput-byte p2, p0, Lpmsj/work/d/a;->s:B

    if-eqz p1, :cond_0

    iget v0, p0, Lpmsj/work/d/a;->k:I

    if-nez v0, :cond_0

    invoke-virtual {p1}, Lpmsj/work/a/i;->c()I

    move-result v0

    iput v0, p0, Lpmsj/work/d/a;->k:I

    invoke-virtual {p1}, Lpmsj/work/a/i;->b()I

    move-result v0

    iput v0, p0, Lpmsj/work/d/a;->l:I

    :cond_0
    return-void
.end method

.method public final a(Lpmsj/work/a/i;Lpmsj/work/a/i;)V
    .locals 0

    iput-object p1, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    iput-object p2, p0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    return-void
.end method

.method public final a(Lpmsj/work/b/j;)V
    .locals 2

    if-nez p1, :cond_0

    :goto_0
    return-void

    :cond_0
    iget v0, p0, Lpmsj/work/d/a;->L:I

    invoke-virtual {p1, v0}, Lpmsj/work/b/j;->c(I)V

    iget-short v0, p1, Lpmsj/work/b/j;->q:S

    invoke-static {v0}, La/c/x;->f(I)Lpmsj/work/a/i;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {p0, v0, v1}, Lpmsj/work/d/a;->a(Lpmsj/work/a/i;B)V

    iget v0, p1, Lpmsj/work/b/j;->f:I

    iput v0, p0, Lpmsj/work/d/a;->b:I

    iget v0, p0, Lpmsj/work/d/a;->b:I

    invoke-virtual {p0, v0}, Lpmsj/work/d/a;->h(I)V

    iget v0, p1, Lpmsj/work/b/j;->e:I

    iput v0, p0, Lpmsj/work/d/a;->a:I

    goto :goto_0
.end method

.method public final a(Lpmsj/work/b/w;)V
    .locals 2

    if-nez p1, :cond_0

    :goto_0
    return-void

    :cond_0
    const/4 v0, 0x4

    invoke-virtual {p1, v0}, Lpmsj/work/b/w;->b(I)I

    move-result v0

    invoke-static {v0}, La/c/x;->e(I)Lpmsj/work/a/i;

    move-result-object v0

    const/4 v1, 0x0

    invoke-virtual {p0, v0, v1}, Lpmsj/work/d/a;->a(Lpmsj/work/a/i;B)V

    const/4 v0, 0x1

    invoke-virtual {p1, v0}, Lpmsj/work/b/w;->b(I)I

    move-result v0

    iput v0, p0, Lpmsj/work/d/a;->a:I

    goto :goto_0
.end method

.method public final a_(Ljava/lang/String;)V
    .locals 1

    iput-object p1, p0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    sget-object v0, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v0, p1}, Ljavax/microedition/lcdui/Font;->a(Ljava/lang/String;)I

    move-result v0

    iput v0, p0, Lpmsj/work/d/a;->d:I

    const/4 v0, 0x0

    iput-object v0, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    const/4 v0, -0x1

    iput v0, p0, Lpmsj/work/d/a;->A:I

    return-void
.end method

.method public final b()Ljava/lang/String;
    .locals 1

    iget-object v0, p0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    return-object v0
.end method

.method public final b(Ljavax/microedition/lcdui/Graphics;II)V
    .locals 19

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v5, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v6, v0

    invoke-static {v5, v6}, Lpmsj/work/d/b;->g(II)Z

    move-result v5

    if-eqz v5, :cond_1

    :cond_0
    :goto_0
    return-void

    :cond_1
    invoke-virtual/range {p0 .. p0}, Lpmsj/work/d/a;->J()Z

    move-result v5

    if-eqz v5, :cond_3

    const/high16 v5, 0x20000

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_3

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->T:Lpmsj/work/a/i;

    move-object v5, v0

    if-nez v5, :cond_2

    new-instance v5, Lpmsj/work/a/i;

    const v6, 0x17a6b0

    invoke-direct {v5, v6}, Lpmsj/work/a/i;-><init>(I)V

    move-object v0, v5

    move-object/from16 v1, p0

    iput-object v0, v1, Lpmsj/work/d/a;->T:Lpmsj/work/a/i;

    :cond_2
    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->T:Lpmsj/work/a/i;

    move-object v6, v0

    invoke-virtual {v6}, Lpmsj/work/a/i;->c()I

    move-result v6

    sub-int v11, v5, v6

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v5, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v6, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->T:Lpmsj/work/a/i;

    move-object v7, v0

    invoke-virtual {v7}, Lpmsj/work/a/i;->b()I

    move-result v7

    sub-int/2addr v6, v7

    div-int/lit8 v6, v6, 0x2

    add-int v8, v5, v6

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->T:Lpmsj/work/a/i;

    move-object v5, v0

    const/4 v6, 0x1

    sub-int v7, v11, v6

    const/4 v9, 0x0

    const/4 v10, 0x0

    move-object/from16 v6, p1

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->T:Lpmsj/work/a/i;

    move-object v5, v0

    add-int/lit8 v6, v11, 0x1

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    add-int/2addr v6, v7

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->T:Lpmsj/work/a/i;

    move-object v7, v0

    invoke-virtual {v7}, Lpmsj/work/a/i;->c()I

    move-result v7

    add-int/2addr v7, v6

    const/4 v9, 0x0

    const/4 v10, 0x2

    move-object/from16 v6, p1

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    :cond_3
    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->h:I

    move v5, v0

    and-int/lit8 v5, v5, 0x10

    if-eqz v5, :cond_4

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->G:I

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->H:I

    move v7, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->I:I

    move v8, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->J:I

    move v9, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->K:I

    move v10, v0

    move-object/from16 v5, p1

    invoke-static/range {v5 .. v10}, La/a/f;->b(Ljavax/microedition/lcdui/Graphics;IIIII)V

    :cond_4
    const/4 v5, 0x0

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/d/a;->H()Z

    move-result v6

    if-nez v6, :cond_12

    const/4 v5, 0x3

    :cond_5
    :goto_1
    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->F:I

    move v6, v0

    if-ltz v6, :cond_6

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->F:I

    move v6, v0

    const/4 v7, 0x3

    if-gt v6, v7, :cond_6

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->F:I

    move v5, v0

    int-to-byte v5, v5

    :cond_6
    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/d/a;->p:B

    move v6, v0

    if-ge v6, v5, :cond_2e

    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/d/a;->p:B

    move v5, v0

    move v13, v5

    :goto_2
    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->h:I

    move v5, v0

    and-int/lit8 v5, v5, 0x2

    if-eqz v5, :cond_17

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    const/4 v6, 0x1

    sub-int v6, v5, v6

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v5, v0

    const/4 v7, 0x1

    sub-int v7, v5, v7

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v8, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v9, v0

    const v10, 0x676767

    move-object/from16 v5, p1

    invoke-static/range {v5 .. v10}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIII)V

    :cond_7
    :goto_3
    const/4 v5, 0x0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v6, v0

    if-eqz v6, :cond_2d

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/a/i;->c()I

    move-result v5

    move v15, v5

    :goto_4
    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move/from16 v16, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->x:Lpmsj/work/a/i;

    move-object v5, v0

    if-eqz v5, :cond_8

    const/high16 v5, 0x10000

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_22

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->x:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->x:Lpmsj/work/a/i;

    move-object v8, v0

    invoke-virtual {v8}, Lpmsj/work/a/i;->c()I

    move-result v8

    sub-int/2addr v7, v8

    div-int/lit8 v7, v7, 0x2

    add-int/2addr v7, v6

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->x:Lpmsj/work/a/i;

    move-object v9, v0

    invoke-virtual {v9}, Lpmsj/work/a/i;->b()I

    move-result v9

    sub-int/2addr v8, v9

    div-int/lit8 v8, v8, 0x2

    add-int/2addr v8, v6

    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/d/a;->y:B

    move v10, v0

    move-object/from16 v6, p1

    move v9, v13

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    :cond_8
    :goto_5
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v5, v0

    if-eqz v5, :cond_a

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->R:Lpmsj/work/a/i;

    move-object v5, v0

    if-eqz v5, :cond_a

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v7, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v5, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->S:I

    move/from16 v17, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v6, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v8, v0

    if-eqz v8, :cond_a

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->R:Lpmsj/work/a/i;

    move-object v8, v0

    if-eqz v8, :cond_a

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v8, v0

    invoke-virtual {v8}, Lpmsj/work/a/i;->b()I

    move-result v8

    sub-int v8, v6, v8

    if-lez v8, :cond_2c

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v8, v0

    invoke-virtual {v8}, Lpmsj/work/a/i;->b()I

    move-result v8

    sub-int/2addr v6, v8

    div-int/lit8 v6, v6, 0x2

    add-int/2addr v5, v6

    move v8, v5

    :goto_6
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/a/i;->c()I

    move-result v5

    move/from16 v0, v17

    move v1, v5

    if-lt v0, v1, :cond_a

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v5, v0

    const/4 v10, 0x0

    move-object/from16 v6, p1

    move v9, v13

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/a/i;->c()I

    move-result v5

    mul-int/lit8 v5, v5, 0x2

    move/from16 v0, v17

    move v1, v5

    if-le v0, v1, :cond_9

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->R:Lpmsj/work/a/i;

    move-object v9, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/a/i;->c()I

    move-result v5

    add-int v10, v7, v5

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/a/i;->c()I

    move-result v5

    mul-int/lit8 v5, v5, 0x2

    sub-int v12, v17, v5

    move v11, v8

    move-object/from16 v14, p1

    invoke-virtual/range {v9 .. v14}, Lpmsj/work/a/i;->a(IIIILjavax/microedition/lcdui/Graphics;)V

    :cond_9
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v5, v0

    add-int v6, v7, v17

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    move-object v7, v0

    invoke-virtual {v7}, Lpmsj/work/a/i;->c()I

    move-result v7

    sub-int v7, v6, v7

    const/4 v10, 0x2

    move-object/from16 v6, p1

    move v9, v13

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    :cond_a
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v5, v0

    if-eqz v5, :cond_b

    const/high16 v5, 0x10000

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_23

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v9, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v6, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v7, v0

    invoke-virtual {v7}, Lpmsj/work/a/i;->c()I

    move-result v7

    sub-int/2addr v6, v7

    div-int/lit8 v6, v6, 0x2

    add-int v11, v5, v6

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v5, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v6, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v7, v0

    invoke-virtual {v7}, Lpmsj/work/a/i;->b()I

    move-result v7

    sub-int/2addr v6, v7

    div-int/lit8 v6, v6, 0x2

    add-int v12, v5, v6

    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/d/a;->s:B

    move v14, v0

    move-object/from16 v10, p1

    invoke-virtual/range {v9 .. v14}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    :cond_b
    :goto_7
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->t:Lpmsj/work/a/i;

    move-object v5, v0

    if-eqz v5, :cond_c

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->t:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v6, v0

    if-eqz v6, :cond_24

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v6, v0

    :goto_8
    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v7, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->t:Lpmsj/work/a/i;

    move-object v9, v0

    invoke-virtual {v9}, Lpmsj/work/a/i;->b()I

    move-result v9

    sub-int/2addr v8, v9

    div-int/lit8 v8, v8, 0x2

    add-int/2addr v7, v8

    move-object v0, v5

    move-object/from16 v1, p1

    move v2, v6

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_c
    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->A:I

    move v5, v0

    const/4 v6, -0x1

    if-eq v5, v6, :cond_25

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    move-object v5, v0

    if-eqz v5, :cond_25

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move-object/from16 v0, p0

    move-object/from16 v1, p1

    move v2, v5

    move v3, v6

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/d/a;->a(Ljavax/microedition/lcdui/Graphics;II)V

    :cond_d
    :goto_9
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->u:La/a/d;

    move-object v5, v0

    if-eqz v5, :cond_10

    move-object/from16 v0, p0

    iget-boolean v0, v0, Lpmsj/work/d/a;->v:Z

    move v5, v0

    if-eqz v5, :cond_2b

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v6, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v7, v0

    invoke-virtual {v7}, Lpmsj/work/a/i;->c()I

    move-result v7

    sub-int/2addr v6, v7

    div-int/lit8 v6, v6, 0x2

    add-int/2addr v5, v6

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v7, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v8, v0

    invoke-virtual {v8}, Lpmsj/work/a/i;->b()I

    move-result v8

    add-int/2addr v7, v8

    div-int/lit8 v7, v7, 0x2

    add-int/2addr v6, v7

    move/from16 v18, v6

    move v6, v5

    move/from16 v5, v18

    :goto_a
    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->e:I

    move v7, v0

    if-nez v7, :cond_e

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->f:I

    move v7, v0

    if-eqz v7, :cond_f

    :cond_e
    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->e:I

    move v7, v0

    add-int/2addr v6, v7

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->f:I

    move v7, v0

    add-int/2addr v5, v7

    :cond_f
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->u:La/a/d;

    move-object v7, v0

    move-object v0, v7

    move v1, v6

    move v2, v5

    move-object/from16 v3, p1

    invoke-virtual {v0, v1, v2, v3}, La/a/d;->b(IILjavax/microedition/lcdui/Graphics;)V

    :cond_10
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v5, v0

    if-nez v5, :cond_11

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->x:Lpmsj/work/a/i;

    move-object v5, v0

    if-nez v5, :cond_11

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->u:La/a/d;

    move-object v5, v0

    if-nez v5, :cond_11

    const/4 v5, 0x2

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-nez v5, :cond_11

    const/16 v5, 0x1000

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-nez v5, :cond_11

    const/16 v5, 0x4000

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_0

    :cond_11
    invoke-virtual/range {p0 .. p0}, Lpmsj/work/d/a;->J()Z

    move-result v5

    if-eqz v5, :cond_0

    const/16 v5, 0x800

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-nez v5, :cond_0

    sget-object v5, Lpmsj/work/d/a;->o:Lpmsj/work/a/b;

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v6, v0

    const/4 v7, 0x2

    sub-int v7, v6, v7

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    const/4 v8, 0x2

    sub-int v8, v6, v8

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v6, v0

    add-int/lit8 v9, v6, 0x4

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v6, v0

    add-int/lit8 v10, v6, 0x4

    move-object/from16 v6, p1

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/b;->a(Ljavax/microedition/lcdui/Graphics;IIII)V

    goto/16 :goto_0

    :cond_12
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->w:La/c/q;

    move-object v6, v0

    invoke-virtual {v6}, La/c/q;->h()Z

    move-result v6

    if-eqz v6, :cond_13

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->w:La/c/q;

    move-object v6, v0

    invoke-virtual {v6}, La/c/q;->i()Z

    move-result v6

    if-eqz v6, :cond_14

    :cond_13
    const/4 v6, -0x1

    move/from16 v0, p2

    move v1, v6

    if-eq v0, v1, :cond_16

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v6, v0

    move/from16 v0, p2

    move v1, v6

    if-lt v0, v1, :cond_16

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/d/a;->F()I

    move-result v6

    move/from16 v0, p2

    move v1, v6

    if-ge v0, v1, :cond_16

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move/from16 v0, p3

    move v1, v6

    if-lt v0, v1, :cond_16

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/d/a;->E()I

    move-result v6

    move/from16 v0, p3

    move v1, v6

    if-ge v0, v1, :cond_16

    :cond_14
    const/16 v5, 0x100

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_15

    const/4 v5, 0x1

    goto/16 :goto_1

    :cond_15
    const/4 v5, 0x1

    goto/16 :goto_1

    :cond_16
    invoke-virtual/range {p0 .. p0}, Lpmsj/work/d/a;->J()Z

    move-result v6

    if-eqz v6, :cond_5

    const/4 v5, 0x1

    goto/16 :goto_1

    :cond_17
    const/16 v5, 0x1000

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_18

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v7, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v8, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v9, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v10, v0

    const/4 v11, 0x0

    move-object/from16 v5, p0

    move-object/from16 v6, p1

    invoke-virtual/range {v5 .. v11}, Lpmsj/work/d/a;->a(Ljavax/microedition/lcdui/Graphics;IIIIB)V

    goto/16 :goto_3

    :cond_18
    const v5, 0x8000

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_1b

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v7, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v8, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v11, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    move-object v5, v0

    if-nez v5, :cond_19

    new-instance v5, Lpmsj/work/a/i;

    const v6, 0x147790

    const/4 v9, 0x0

    invoke-direct {v5, v6, v9}, Lpmsj/work/a/i;-><init>(II)V

    move-object v0, v5

    move-object/from16 v1, p0

    iput-object v0, v1, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    :cond_19
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    move-object v5, v0

    if-nez v5, :cond_1a

    new-instance v5, Lpmsj/work/a/i;

    const v6, 0x147664

    const/4 v9, 0x0

    invoke-direct {v5, v6, v9}, Lpmsj/work/a/i;-><init>(II)V

    move-object v0, v5

    move-object/from16 v1, p0

    iput-object v0, v1, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    :cond_1a
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    move-object v5, v0

    const/4 v9, 0x0

    const/4 v10, 0x0

    move-object/from16 v6, p1

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    move-object v6, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/a/i;->c()I

    move-result v5

    add-int/2addr v7, v5

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    move-object v5, v0

    invoke-virtual {v5}, Lpmsj/work/a/i;->c()I

    move-result v5

    sub-int v9, v11, v5

    const/4 v10, 0x0

    move-object/from16 v11, p1

    invoke-virtual/range {v6 .. v11}, Lpmsj/work/a/i;->a(IIIILjavax/microedition/lcdui/Graphics;)V

    goto/16 :goto_3

    :cond_1b
    const/16 v5, 0x2000

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_1c

    new-instance v5, Lpmsj/work/a/i;

    const v6, 0x149bdb

    invoke-direct {v5, v6}, Lpmsj/work/a/i;-><init>(I)V

    new-instance v11, Lpmsj/work/a/i;

    const v6, 0x149ca3

    invoke-direct {v11, v6}, Lpmsj/work/a/i;-><init>(I)V

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v7, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v8, v0

    const/4 v9, 0x0

    const/4 v10, 0x0

    move-object/from16 v6, p1

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v6, v0

    invoke-virtual {v5}, Lpmsj/work/a/i;->c()I

    move-result v7

    add-int/2addr v6, v7

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v7, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v8, v0

    invoke-virtual {v5}, Lpmsj/work/a/i;->c()I

    move-result v5

    mul-int/lit8 v5, v5, 0x2

    sub-int/2addr v8, v5

    const/4 v9, 0x0

    move-object v5, v11

    move-object/from16 v10, p1

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->a(IIIILjavax/microedition/lcdui/Graphics;)V

    goto/16 :goto_3

    :cond_1c
    const/16 v5, 0x4000

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_1d

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v7, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v8, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    move-object v5, v0

    if-eqz v5, :cond_7

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    move-object v5, v0

    const/4 v10, 0x0

    move-object/from16 v6, p1

    move v9, v13

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    move-object v6, v0

    invoke-virtual {v6}, Lpmsj/work/a/i;->c()I

    move-result v6

    add-int/2addr v7, v6

    const/4 v10, 0x2

    move-object/from16 v6, p1

    move v9, v13

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    goto/16 :goto_3

    :cond_1d
    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->h:I

    move v5, v0

    and-int/lit8 v5, v5, 0x4

    if-eqz v5, :cond_1f

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/d/a;->J()Z

    move-result v5

    if-nez v5, :cond_1e

    const/4 v5, 0x0

    move-object/from16 v0, p1

    move v1, v5

    invoke-virtual {v0, v1}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    move-object/from16 v0, p1

    move v1, v5

    move v2, v6

    move v3, v7

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Ljavax/microedition/lcdui/Graphics;->c(IIII)V

    sget v5, Lpmsj/work/a/c;->Q:I

    move-object/from16 v0, p1

    move v1, v5

    invoke-virtual {v0, v1}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    move-object/from16 v0, p1

    move v1, v5

    move v2, v6

    move v3, v7

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Ljavax/microedition/lcdui/Graphics;->b(IIII)V

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    add-int/lit8 v5, v5, 0x1

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    add-int/lit8 v6, v6, 0x1

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    const/4 v8, 0x2

    sub-int/2addr v7, v8

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    const/4 v9, 0x2

    sub-int/2addr v8, v9

    move-object/from16 v0, p1

    move v1, v5

    move v2, v6

    move v3, v7

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Ljavax/microedition/lcdui/Graphics;->b(IIII)V

    goto/16 :goto_3

    :cond_1e
    const v5, 0x222222

    move-object/from16 v0, p1

    move v1, v5

    invoke-virtual {v0, v1}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    move-object/from16 v0, p1

    move v1, v5

    move v2, v6

    move v3, v7

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Ljavax/microedition/lcdui/Graphics;->c(IIII)V

    sget v5, Lpmsj/work/a/c;->T:I

    move-object/from16 v0, p1

    move v1, v5

    invoke-virtual {v0, v1}, Ljavax/microedition/lcdui/Graphics;->a(I)V

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    move-object/from16 v0, p1

    move v1, v5

    move v2, v6

    move v3, v7

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Ljavax/microedition/lcdui/Graphics;->b(IIII)V

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    add-int/lit8 v5, v5, 0x1

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    add-int/lit8 v6, v6, 0x1

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    const/4 v8, 0x2

    sub-int/2addr v7, v8

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    const/4 v9, 0x2

    sub-int/2addr v8, v9

    move-object/from16 v0, p1

    move v1, v5

    move v2, v6

    move v3, v7

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Ljavax/microedition/lcdui/Graphics;->b(IIII)V

    goto/16 :goto_3

    :cond_1f
    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->h:I

    move v5, v0

    and-int/lit8 v5, v5, 0x8

    if-nez v5, :cond_7

    const/high16 v5, 0x40000

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_7

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    move-object v5, v0

    if-eqz v5, :cond_20

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    move-object v5, v0

    if-eqz v5, :cond_20

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v7, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v8, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v9, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v10, v0

    move-object/from16 v5, p0

    move-object/from16 v6, p1

    move v11, v13

    invoke-virtual/range {v5 .. v11}, Lpmsj/work/d/a;->a(Ljavax/microedition/lcdui/Graphics;IIIIB)V

    goto/16 :goto_3

    :cond_20
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v5, v0

    if-nez v5, :cond_7

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->x:Lpmsj/work/a/i;

    move-object v5, v0

    if-nez v5, :cond_7

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->M:Lpmsj/work/a/i;

    move-object v5, v0

    if-eqz v5, :cond_21

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->M:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->M:Lpmsj/work/a/i;

    move-object v8, v0

    invoke-virtual {v8}, Lpmsj/work/a/i;->c()I

    move-result v8

    sub-int/2addr v7, v8

    div-int/lit8 v7, v7, 0x2

    add-int/2addr v7, v6

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->M:Lpmsj/work/a/i;

    move-object v9, v0

    invoke-virtual {v9}, Lpmsj/work/a/i;->b()I

    move-result v9

    sub-int/2addr v8, v9

    div-int/lit8 v8, v8, 0x2

    add-int/2addr v8, v6

    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/d/a;->N:B

    move v10, v0

    move-object/from16 v6, p1

    move v9, v13

    invoke-virtual/range {v5 .. v10}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;IIII)V

    goto/16 :goto_3

    :cond_21
    const/16 v5, 0x200

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-nez v5, :cond_7

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    move-object/from16 v0, p1

    move v1, v5

    move v2, v6

    move v3, v7

    move v4, v13

    invoke-static {v0, v1, v2, v3, v4}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;IIIB)V

    goto/16 :goto_3

    :cond_22
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->x:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->x:Lpmsj/work/a/i;

    move-object v8, v0

    invoke-virtual {v8}, Lpmsj/work/a/i;->c()I

    move-result v8

    sub-int/2addr v7, v8

    div-int/lit8 v7, v7, 0x2

    add-int/2addr v6, v7

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v7, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->x:Lpmsj/work/a/i;

    move-object v9, v0

    invoke-virtual {v9}, Lpmsj/work/a/i;->b()I

    move-result v9

    sub-int/2addr v8, v9

    div-int/lit8 v8, v8, 0x2

    add-int/2addr v7, v8

    move-object v0, v5

    move-object/from16 v1, p1

    move v2, v6

    move v3, v7

    invoke-virtual {v0, v1, v2, v3}, Lpmsj/work/a/i;->b(Ljavax/microedition/lcdui/Graphics;II)V

    goto/16 :goto_5

    :cond_23
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v5, v0

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v7, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v8, v0

    invoke-virtual {v8}, Lpmsj/work/a/i;->c()I

    move-result v8

    sub-int/2addr v7, v8

    div-int/lit8 v7, v7, 0x2

    add-int/2addr v6, v7

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v7, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v8, v0

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    move-object v9, v0

    invoke-virtual {v9}, Lpmsj/work/a/i;->b()I

    move-result v9

    sub-int/2addr v8, v9

    div-int/lit8 v8, v8, 0x2

    add-int/2addr v7, v8

    move-object/from16 v0, p0

    iget-byte v0, v0, Lpmsj/work/d/a;->s:B

    move v8, v0

    move-object v0, v5

    move-object/from16 v1, p1

    move v2, v6

    move v3, v7

    move v4, v8

    invoke-virtual {v0, v1, v2, v3, v4}, Lpmsj/work/a/i;->a(Ljavax/microedition/lcdui/Graphics;III)V

    goto/16 :goto_7

    :cond_24
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->t:Lpmsj/work/a/i;

    move-object v6, v0

    invoke-virtual {v6}, Lpmsj/work/a/i;->c()I

    move-result v6

    sub-int v6, v16, v6

    goto/16 :goto_8

    :cond_25
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    move-object v5, v0

    if-eqz v5, :cond_d

    const-string v5, ""

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    move-object v6, v0

    invoke-virtual {v5, v6}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v5

    if-nez v5, :cond_d

    const/4 v5, 0x0

    const/high16 v6, 0x800000

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->h:I

    move v7, v0

    and-int/2addr v6, v7

    if-eqz v6, :cond_26

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    move-object v6, v0

    invoke-virtual {v6}, Ljava/lang/String;->length()I

    move-result v6

    if-lez v6, :cond_26

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v5, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->d:I

    move v6, v0

    sub-int/2addr v5, v6

    shr-int/lit8 v5, v5, 0x1

    :cond_26
    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v6, v0

    add-int/2addr v5, v6

    add-int v11, v5, v15

    const/16 v5, 0x400

    move-object/from16 v0, p0

    move v1, v5

    invoke-virtual {v0, v1}, Lpmsj/work/d/a;->k(I)Z

    move-result v5

    if-eqz v5, :cond_29

    invoke-virtual/range {p0 .. p0}, Lpmsj/work/d/a;->J()Z

    move-result v5

    if-eqz v5, :cond_27

    add-int/lit8 v6, v11, 0x3

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v5, v0

    add-int/lit8 v7, v5, 0x4

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v8, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v9, v0

    sget v10, Lpmsj/work/a/c;->I:I

    move-object/from16 v5, p1

    invoke-static/range {v5 .. v10}, La/c/x;->b(Ljavax/microedition/lcdui/Graphics;IIIII)V

    :cond_27
    invoke-virtual/range {p0 .. p0}, Lpmsj/work/d/a;->J()Z

    move-result v5

    if-eqz v5, :cond_28

    sget v5, Lpmsj/work/a/c;->J:I

    move v10, v5

    :goto_b
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    move-object v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->C:I

    move v5, v0

    add-int/2addr v5, v11

    add-int/lit8 v7, v5, 0x3

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v5, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->D:I

    move v8, v0

    add-int/2addr v8, v5

    sget-object v9, Lpmsj/work/a/c;->ab:Ljavax/microedition/lcdui/Font;

    const/4 v11, 0x0

    move-object/from16 v5, p1

    invoke-static/range {v5 .. v11}, La/c/x;->a(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;IILjavax/microedition/lcdui/Font;II)V

    sget-object v5, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    move-object/from16 v0, p1

    move-object v1, v5

    invoke-virtual {v0, v1}, Ljavax/microedition/lcdui/Graphics;->a(Ljavax/microedition/lcdui/Font;)V

    goto/16 :goto_9

    :cond_28
    sget v5, Lpmsj/work/a/c;->H:I

    move v10, v5

    goto :goto_b

    :cond_29
    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v5, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v6, v0

    sget-object v7, Lpmsj/work/a/c;->aa:Ljavax/microedition/lcdui/Font;

    invoke-virtual {v7}, Ljavax/microedition/lcdui/Font;->e()I

    move-result v7

    sub-int/2addr v6, v7

    sget v7, La/c/x;->c:I

    add-int/2addr v6, v7

    shr-int/lit8 v6, v6, 0x1

    add-int/2addr v5, v6

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->w:La/c/q;

    move-object v6, v0

    invoke-virtual {v6}, La/c/q;->h()Z

    move-result v6

    if-eqz v6, :cond_2a

    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->w:La/c/q;

    move-object v6, v0

    invoke-virtual {v6}, La/c/q;->i()Z

    move-result v6

    if-nez v6, :cond_2a

    add-int/lit8 v5, v5, 0x2

    :cond_2a
    move-object/from16 v0, p0

    iget-object v0, v0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    move-object v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->C:I

    move v7, v0

    add-int/2addr v7, v11

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->D:I

    move v8, v0

    add-int/2addr v5, v8

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->m:I

    move v8, v0

    move-object/from16 v0, p1

    move-object v1, v6

    move v2, v7

    move v3, v5

    move v4, v8

    invoke-static {v0, v1, v2, v3, v4}, La/c/x;->b(Ljavax/microedition/lcdui/Graphics;Ljava/lang/String;III)V

    goto/16 :goto_9

    :cond_2b
    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->i:S

    move v5, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->k:I

    move v6, v0

    div-int/lit8 v6, v6, 0x2

    add-int/2addr v5, v6

    move-object/from16 v0, p0

    iget-short v0, v0, Lpmsj/work/d/a;->j:S

    move v6, v0

    move-object/from16 v0, p0

    iget v0, v0, Lpmsj/work/d/a;->l:I

    move v7, v0

    add-int/2addr v6, v7

    const/16 v7, 0xa

    sub-int/2addr v6, v7

    move/from16 v18, v6

    move v6, v5

    move/from16 v5, v18

    goto/16 :goto_a

    :cond_2c
    move v8, v5

    goto/16 :goto_6

    :cond_2d
    move v15, v5

    goto/16 :goto_4

    :cond_2e
    move v13, v5

    goto/16 :goto_2
.end method

.method public final b(Lpmsj/work/a/i;)V
    .locals 0

    iput-object p1, p0, Lpmsj/work/d/a;->x:Lpmsj/work/a/i;

    return-void
.end method

.method public final b(Lpmsj/work/a/i;B)V
    .locals 0

    iput-object p1, p0, Lpmsj/work/d/a;->M:Lpmsj/work/a/i;

    iput-byte p2, p0, Lpmsj/work/d/a;->N:B

    return-void
.end method

.method public final b(Lpmsj/work/a/i;Lpmsj/work/a/i;)V
    .locals 0

    iput-object p1, p0, Lpmsj/work/d/a;->Q:Lpmsj/work/a/i;

    iput-object p2, p0, Lpmsj/work/d/a;->R:Lpmsj/work/a/i;

    return-void
.end method

.method public final b(II)Z
    .locals 1

    invoke-virtual {p0}, Lpmsj/work/d/a;->J()Z

    move-result v0

    if-eqz v0, :cond_0

    const/16 v0, 0x8

    invoke-virtual {p0, v0}, Lpmsj/work/d/a;->a(B)V

    :cond_0
    const/4 v0, 0x1

    return v0
.end method

.method public final c()V
    .locals 2

    iget-object v0, p0, Lpmsj/work/d/a;->w:La/c/q;

    const/16 v1, 0xfa

    invoke-virtual {v0, v1}, La/c/q;->e(I)V

    return-void
.end method

.method public final c(I)V
    .locals 0

    iput p1, p0, Lpmsj/work/d/a;->F:I

    return-void
.end method

.method public final c(Lpmsj/work/a/i;)V
    .locals 1

    const/4 v0, 0x0

    invoke-virtual {p0, p1, v0}, Lpmsj/work/d/a;->a(Lpmsj/work/a/i;B)V

    return-void
.end method

.method public final c_()B
    .locals 1

    const/4 v0, 0x2

    return v0
.end method

.method public final d()I
    .locals 1

    iget v0, p0, Lpmsj/work/d/a;->a:I

    return v0
.end method

.method public final d(I)Z
    .locals 2

    iget-object v0, p0, Lpmsj/work/d/a;->w:La/c/q;

    const/16 v1, 0xfa

    invoke-virtual {v0, v1}, La/c/q;->e(I)V

    invoke-super {p0, p1}, Lpmsj/work/d/b;->d(I)Z

    move-result v0

    return v0
.end method

.method public final e()I
    .locals 1

    iget v0, p0, Lpmsj/work/d/a;->b:I

    return v0
.end method

.method public final e(I)Z
    .locals 2

    sget-object v0, Lpmsj/work/a/c;->Z:[S

    const/4 v1, 0x6

    aget-short v0, v0, v1

    if-eq p1, v0, :cond_0

    sget-object v0, Lpmsj/work/a/c;->Z:[S

    const/4 v1, 0x1

    aget-short v0, v0, v1

    if-ne p1, v0, :cond_1

    :cond_0
    iget-object v0, p0, Lpmsj/work/d/a;->w:La/c/q;

    const/16 v1, 0xfa

    invoke-virtual {v0, v1}, La/c/q;->e(I)V

    :cond_1
    invoke-super {p0, p1}, Lpmsj/work/d/b;->e(I)Z

    move-result v0

    return v0
.end method

.method public final f()V
    .locals 2

    const/4 v1, 0x0

    iput-object v1, p0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    const/4 v0, 0x0

    iput v0, p0, Lpmsj/work/d/a;->a:I

    iput-object v1, p0, Lpmsj/work/d/a;->u:La/a/d;

    iput-object v1, p0, Lpmsj/work/d/a;->O:Lpmsj/work/a/i;

    iput-object v1, p0, Lpmsj/work/d/a;->P:Lpmsj/work/a/i;

    const/4 v0, -0x1

    iput v0, p0, Lpmsj/work/d/a;->A:I

    iput-object v1, p0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    return-void
.end method

.method public final f(I)V
    .locals 2

    sget-object v0, Lpmsj/work/a/c;->Z:[S

    const/4 v1, 0x6

    aget-short v0, v0, v1

    if-eq p1, v0, :cond_0

    sget-object v0, Lpmsj/work/a/c;->Z:[S

    const/4 v1, 0x1

    aget-short v0, v0, v1

    if-ne p1, v0, :cond_1

    :cond_0
    invoke-virtual {p0}, Lpmsj/work/d/a;->v()V

    const/16 v0, 0x8

    invoke-virtual {p0, v0}, Lpmsj/work/d/a;->a(B)V

    :cond_1
    return-void
.end method

.method public final g()V
    .locals 2

    const/4 v1, 0x0

    iput-object v1, p0, Lpmsj/work/d/a;->r:Lpmsj/work/a/i;

    const/4 v0, 0x0

    iput v0, p0, Lpmsj/work/d/a;->a:I

    iput-object v1, p0, Lpmsj/work/d/a;->u:La/a/d;

    return-void
.end method

.method public final g(I)V
    .locals 0

    iput p1, p0, Lpmsj/work/d/a;->S:I

    return-void
.end method

.method public final h()V
    .locals 1

    const/4 v0, 0x0

    iput-object v0, p0, Lpmsj/work/d/a;->c:Ljava/lang/String;

    iput-object v0, p0, Lpmsj/work/d/a;->z:Lpmsj/work/d/e;

    const/4 v0, -0x1

    iput v0, p0, Lpmsj/work/d/a;->A:I

    return-void
.end method

.method public final h(I)V
    .locals 5

    const/4 v4, 0x1

    const/4 v3, 0x0

    invoke-static {p1}, Lpmsj/work/b/g;->j(I)I

    move-result v0

    if-lez v0, :cond_1

    invoke-static {p1}, Lpmsj/work/b/j;->g(I)Z

    move-result v1

    if-eqz v1, :cond_1

    iget v1, p0, Lpmsj/work/d/a;->L:I

    sget v2, La/c/x;->b:I

    if-ne v1, v2, :cond_0

    const v1, 0x1ef9b0

    invoke-static {v1, v3}, La/a/d;->a(IZ)La/a/d;

    move-result-object v1

    iput-object v1, p0, Lpmsj/work/d/a;->u:La/a/d;

    :goto_0
    iget-object v1, p0, Lpmsj/work/d/a;->u:La/a/d;

    sub-int/2addr v0, v4

    invoke-virtual {v1, v0}, La/a/d;->d(I)V

    iput-boolean v4, p0, Lpmsj/work/d/a;->v:Z

    :goto_1
    return-void

    :cond_0
    const v1, 0x1ed2a0

    invoke-static {v1, v3}, La/a/d;->a(IZ)La/a/d;

    move-result-object v1

    iput-object v1, p0, Lpmsj/work/d/a;->u:La/a/d;

    goto :goto_0

    :cond_1
    const/4 v0, 0x0

    iput-object v0, p0, Lpmsj/work/d/a;->u:La/a/d;

    iput-boolean v3, p0, Lpmsj/work/d/a;->v:Z

    goto :goto_1
.end method

.method public final i()La/a/d;
    .locals 1

    iget-object v0, p0, Lpmsj/work/d/a;->u:La/a/d;

    return-object v0
.end method

.method public final i(I)V
    .locals 1

    const/4 v0, 0x0

    iput v0, p0, Lpmsj/work/d/a;->e:I

    iput p1, p0, Lpmsj/work/d/a;->f:I

    return-void
.end method

.method public final j()V
    .locals 2

    const v0, 0x1ef9b0

    const/4 v1, 0x0

    invoke-static {v0, v1}, La/a/d;->a(IZ)La/a/d;

    move-result-object v0

    iput-object v0, p0, Lpmsj/work/d/a;->u:La/a/d;

    iget-object v0, p0, Lpmsj/work/d/a;->u:La/a/d;

    const/4 v1, 0x3

    invoke-virtual {v0, v1}, La/a/d;->d(I)V

    const/4 v0, 0x1

    iput-boolean v0, p0, Lpmsj/work/d/a;->v:Z

    return-void
.end method
